"""Regras de OS, caixa e leitura. Toda listagem de caixa leva entidade."""

from __future__ import annotations

import re
import sqlite3
from datetime import date
from pathlib import Path

from core.backup import criar_backup
from core.cnpj import normalizar_cnpj
from core.entities import (
    STATUS_EXIGE_EVIDENCIA,
    STATUS_INICIAL_EQUIPAMENTO,
    STATUS_INICIAL_OS,
    assert_transicao,
    resolver_centro,
    validar_entidade,
    validar_tipo_equipamento,
)
from core.errors import IntegrityFailure, NotFoundError, TransitionError, ValidationError
from core.evidencia import texto_obrigatorio, validar_ref_tipada
from core.export_bi import csv_centros, csv_consolidado, csv_heros, validar_anomes
from core.preco import interpretar_preco, interpretar_recebido
from core.rna_atlas import gerar_caminho
from db.connection import init_db, session, traduzir_integrity

_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _obrigatorio(valor: str | None, campo: str) -> str:
    texto = "" if valor is None else str(valor).strip()
    if not texto:
        raise ValidationError(f"{campo} obrigatorio")
    return texto


def _opcional(valor: str | None) -> str | None:
    if valor is None:
        return None
    texto = str(valor).strip()
    return texto or None


def _email(valor: str | None) -> str | None:
    texto = _opcional(valor)
    if texto is None:
        return None
    if not _EMAIL.fullmatch(texto):
        raise ValidationError("email fiscal invalido")
    return texto


def _data(valor: date | str, campo: str) -> str:
    if isinstance(valor, date):
        return valor.isoformat()
    texto = str(valor).strip()
    if not _ISO.fullmatch(texto):
        raise ValidationError(f"{campo} invalida")
    try:
        date.fromisoformat(texto)
    except ValueError as exc:
        raise ValidationError(f"{campo} invalida") from exc
    return texto


def _novo_id_os(conn: sqlite3.Connection, entidade: str, ano: int) -> str:
    """{ENTIDADE}-{AAAA}-{NNN}, sequência da entidade naquele ano."""
    if ano < 1000 or ano > 9999:
        raise ValidationError("ano da OS invalido")
    padrao = re.compile(rf"^{re.escape(entidade)}-{ano}-(\d{{3}})$")
    linhas = conn.execute(
        "SELECT id_os FROM ordens_servico WHERE entidade = ?",
        (entidade,),
    ).fetchall()
    numeros = []
    for linha in linhas:
        encontrado = padrao.fullmatch(str(linha[0]))
        if encontrado:
            numeros.append(int(encontrado.group(1)))
    proximo = (max(numeros) if numeros else 0) + 1
    if proximo > 999:
        raise ValidationError("sequencia anual de OS esgotada")
    return f"{entidade}-{ano}-{proximo:03d}"


def _novo_id(conn: sqlite3.Connection, tabela: str, coluna: str, prefixo: str) -> str:
    if tabela not in {"clientes_b2b", "equipamentos", "ordens_servico", "recebimentos", "medicoes"}:
        raise ValidationError("tabela desconhecida")
    if coluna not in {"id_cliente", "id_equipamento", "id_os", "id"}:
        raise ValidationError("coluna desconhecida")
    linhas = conn.execute(
        f"SELECT {coluna} FROM {tabela} WHERE {coluna} LIKE ?",
        (prefixo + "%",),
    ).fetchall()
    numeros = []
    for linha in linhas:
        cauda = str(linha[0]).removeprefix(prefixo)
        if cauda.isdigit():
            numeros.append(int(cauda))
    return f"{prefixo}{(max(numeros) if numeros else 0) + 1:04d}"


def _uma(conn: sqlite3.Connection, sql: str, params: tuple) -> dict | None:
    linha = conn.execute(sql, params).fetchone()
    return None if linha is None else dict(linha)


class GfRepository:
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        init_db(self.db_path)

    def foreign_keys_ativas(self) -> int:
        with session(self.db_path) as conn:
            return int(conn.execute("PRAGMA foreign_keys").fetchone()[0])

    def criar_cliente(
        self,
        *,
        entidade: str,
        razao_social: str,
        cnpj: str,
        inscricao_estadual: str | None = None,
        contato_responsavel: str | None = None,
        telefone: str | None = None,
        email_fiscal: str | None = None,
        endereco: str | None = None,
        observacoes: str | None = None,
    ) -> dict:
        tag = validar_entidade(entidade)
        razao = _obrigatorio(razao_social, "razao_social")
        documento = normalizar_cnpj(cnpj)
        with session(self.db_path) as conn:
            id_cliente = _novo_id(conn, "clientes_b2b", "id_cliente", f"CLI-{tag}-")
            try:
                conn.execute(
                    """
                    INSERT INTO clientes_b2b (
                        id_cliente, entidade, razao_social, cnpj, inscricao_estadual,
                        contato_responsavel, telefone, email_fiscal, endereco, observacoes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        id_cliente,
                        tag,
                        razao,
                        documento,
                        _opcional(inscricao_estadual),
                        _opcional(contato_responsavel),
                        _opcional(telefone),
                        _email(email_fiscal),
                        _opcional(endereco),
                        _opcional(observacoes),
                    ),
                )
            except sqlite3.IntegrityError as exc:
                raise traduzir_integrity(exc) from exc
            return _uma(conn, "SELECT * FROM clientes_b2b WHERE id_cliente = ?", (id_cliente,))

    def criar_equipamento(
        self,
        *,
        entidade: str,
        id_cliente: str,
        tipo_equipamento: str,
        numero_serie: str,
        marca_modelo: str | None = None,
        potencia_especificacao: str | None = None,
    ) -> dict:
        tag = validar_entidade(entidade)
        tipo = validar_tipo_equipamento(tipo_equipamento)
        serie = texto_obrigatorio(numero_serie, "numero_serie")
        with session(self.db_path) as conn:
            cliente = _uma(
                conn,
                "SELECT * FROM clientes_b2b WHERE id_cliente = ? AND entidade = ?",
                (id_cliente, tag),
            )
            if cliente is None:
                raise NotFoundError("cliente nao encontrado nesta entidade")
            id_equipamento = _novo_id(conn, "equipamentos", "id_equipamento", f"EQ-{tag}-")
            try:
                conn.execute(
                    """
                    INSERT INTO equipamentos (
                        id_equipamento, id_cliente, entidade, tipo_equipamento, marca_modelo,
                        numero_serie, potencia_especificacao, status_atual
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        id_equipamento,
                        id_cliente,
                        tag,
                        tipo,
                        _opcional(marca_modelo),
                        serie,
                        _opcional(potencia_especificacao),
                        STATUS_INICIAL_EQUIPAMENTO,
                    ),
                )
            except sqlite3.IntegrityError as exc:
                raise traduzir_integrity(exc) from exc
            return _uma(
                conn,
                "SELECT * FROM equipamentos WHERE id_equipamento = ?",
                (id_equipamento,),
            )

    def abrir_os(
        self,
        *,
        entidade: str,
        id_cliente: str,
        id_equipamento: str,
        data_abertura: date | str,
        descricao_servico: str | None = None,
        data_previsao: date | str | None = None,
        valor_orcamento: float | str | None = None,
        valor_final: float | str | None = None,
        centro_custo: str | None = None,
        responsavel_tecnico: str | None = None,
        quando: date | None = None,
    ) -> dict:
        tag = validar_entidade(entidade)
        centro = resolver_centro(tag, centro_custo)
        abertura = _data(data_abertura, "data_abertura")
        previsao = None if data_previsao in (None, "") else _data(data_previsao, "data_previsao")
        with session(self.db_path) as conn:
            cliente = _uma(
                conn,
                "SELECT id_cliente FROM clientes_b2b WHERE id_cliente = ? AND entidade = ?",
                (id_cliente, tag),
            )
            if cliente is None:
                raise NotFoundError("cliente nao encontrado nesta entidade")
            equipamento = _uma(
                conn,
                "SELECT * FROM equipamentos WHERE id_equipamento = ? AND entidade = ?",
                (id_equipamento, tag),
            )
            if equipamento is None:
                raise NotFoundError("equipamento nao encontrado nesta entidade")
            if equipamento["id_cliente"] != id_cliente:
                raise IntegrityFailure("equipamento nao pertence ao cliente")
            links = [linha[0] for linha in conn.execute("SELECT link_pasta_drive FROM ordens_servico").fetchall()]
            dia_pasta = quando or date.fromisoformat(abertura)
            link = gerar_caminho(
                tag,
                f"Pasta {equipamento['tipo_equipamento']}",
                "dir",
                quando=dia_pasta,
                existentes=links,
            )
            id_os = _novo_id_os(conn, tag, int(abertura[:4]))
            try:
                conn.execute(
                    """
                    INSERT INTO ordens_servico (
                        id_os, id_cliente, id_equipamento, entidade, data_abertura, data_previsao,
                        descricao_servico, status_os, valor_orcamento, valor_final, centro_custo,
                        responsavel_tecnico, link_pasta_drive
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        id_os,
                        id_cliente,
                        id_equipamento,
                        tag,
                        abertura,
                        previsao,
                        _opcional(descricao_servico),
                        STATUS_INICIAL_OS,
                        interpretar_preco(valor_orcamento, "valor_orcamento"),
                        interpretar_preco(valor_final, "valor_final"),
                        centro,
                        _opcional(responsavel_tecnico),
                        link,
                    ),
                )
            except sqlite3.IntegrityError as exc:
                raise traduzir_integrity(exc) from exc
            return _uma(conn, "SELECT * FROM ordens_servico WHERE id_os = ?", (id_os,))

    def obter_os(self, id_os: str, *, entidade: str) -> dict:
        tag = validar_entidade(entidade)
        with session(self.db_path) as conn:
            linha = _uma(
                conn,
                "SELECT * FROM ordens_servico WHERE id_os = ? AND entidade = ?",
                (id_os, tag),
            )
        if linha is None:
            raise NotFoundError("OS nao encontrada nesta entidade")
        return linha

    def transicionar_os(
        self,
        id_os: str,
        status_destino: str,
        *,
        entidade: str,
        quando: date | str | None = None,
    ) -> dict:
        atual = self.obter_os(id_os, entidade=entidade)
        assert_transicao(atual["status_os"], status_destino)
        dia = date.today().isoformat() if quando is None else _data(quando, "data da transicao")
        if dia < atual["data_abertura"]:
            raise ValidationError("data da transicao anterior a abertura")
        with session(self.db_path) as conn:
            if status_destino in STATUS_EXIGE_EVIDENCIA:
                self._exigir_evidencia(conn, atual["id_os"], atual["entidade"])
            try:
                if status_destino == "Faturado":
                    conn.execute(
                        """
                        UPDATE ordens_servico
                        SET status_os = ?, data_conclusao = ?
                        WHERE id_os = ? AND entidade = ?
                        """,
                        (status_destino, dia, id_os, atual["entidade"]),
                    )
                else:
                    conn.execute(
                        """
                        UPDATE ordens_servico
                        SET status_os = ?
                        WHERE id_os = ? AND entidade = ?
                        """,
                        (status_destino, id_os, atual["entidade"]),
                    )
            except sqlite3.IntegrityError as exc:
                raise traduzir_integrity(exc) from exc
        return self.obter_os(id_os, entidade=entidade)

    def definir_valores(
        self,
        id_os: str,
        *,
        entidade: str,
        valor_orcamento: float | None = None,
        valor_final: float | None = None,
    ) -> dict:
        atual = self.obter_os(id_os, entidade=entidade)
        if atual["status_os"] == "Faturado":
            raise TransitionError("OS faturada nao altera valores")
        orcamento = (
            atual["valor_orcamento"]
            if valor_orcamento is None
            else interpretar_preco(valor_orcamento, "valor_orcamento")
        )
        final = atual["valor_final"] if valor_final is None else interpretar_preco(valor_final, "valor_final")
        with session(self.db_path) as conn:
            try:
                conn.execute(
                    """
                    UPDATE ordens_servico
                    SET valor_orcamento = ?, valor_final = ?
                    WHERE id_os = ? AND entidade = ?
                    """,
                    (orcamento, final, id_os, atual["entidade"]),
                )
            except sqlite3.IntegrityError as exc:
                raise traduzir_integrity(exc) from exc
        return self.obter_os(id_os, entidade=entidade)

    def listar_clientes(self, entidade: str) -> list[dict]:
        tag = validar_entidade(entidade)
        with session(self.db_path) as conn:
            linhas = conn.execute(
                "SELECT * FROM clientes_b2b WHERE entidade = ? ORDER BY id_cliente",
                (tag,),
            ).fetchall()
        return [dict(linha) for linha in linhas]

    def listar_equipamentos(self, entidade: str, id_cliente: str | None = None) -> list[dict]:
        tag = validar_entidade(entidade)
        sql = "SELECT * FROM equipamentos WHERE entidade = ?"
        params: list[str] = [tag]
        if id_cliente:
            sql += " AND id_cliente = ?"
            params.append(id_cliente)
        sql += " ORDER BY id_equipamento"
        with session(self.db_path) as conn:
            linhas = conn.execute(sql, params).fetchall()
        return [dict(linha) for linha in linhas]

    def listar_os(self, entidade: str, status_os: str | None = None) -> list[dict]:
        tag = validar_entidade(entidade)
        sql = "SELECT * FROM ordens_servico WHERE entidade = ?"
        params: list[str] = [tag]
        if status_os:
            sql += " AND status_os = ?"
            params.append(status_os)
        sql += " ORDER BY id_os"
        with session(self.db_path) as conn:
            linhas = conn.execute(sql, params).fetchall()
        return [dict(linha) for linha in linhas]

    def _faturadas(self, entidade: str) -> list[dict]:
        tag = validar_entidade(entidade)
        with session(self.db_path) as conn:
            linhas = conn.execute(
                """
                SELECT * FROM ordens_servico
                WHERE entidade = ? AND status_os = 'Faturado'
                ORDER BY data_conclusao, id_os
                """,
                (tag,),
            ).fetchall()
        return [dict(linha) for linha in linhas]

    def exportar_csv_centros(self, entidade: str) -> str:
        return csv_centros(entidade, self._faturadas(entidade))

    def exportar_csv_heros(self, entidade: str) -> str:
        return csv_heros(entidade, self._faturadas(entidade))

    def exportar_csv_operacional(self, entidade: str) -> str:
        return self.exportar_csv_heros(entidade)

    def exportar_csv_consolidado(self, entidade: str, anomes: str | None = None) -> str:
        if anomes:
            validar_anomes(anomes)
        return csv_consolidado(entidade, self._faturadas(entidade), anomes)

    def _exigir_evidencia(self, conn: sqlite3.Connection, id_os: str, entidade: str) -> None:
        medicoes = conn.execute(
            "SELECT COUNT(*) FROM medicoes WHERE id_os = ? AND entidade = ?",
            (id_os, entidade),
        ).fetchone()[0]
        foto = conn.execute(
            "SELECT ref_foto_tipada FROM ordens_servico WHERE id_os = ? AND entidade = ?",
            (id_os, entidade),
        ).fetchone()
        ref = "" if foto is None or foto[0] is None else str(foto[0]).strip()
        if medicoes < 1:
            raise ValidationError("transicao exige medicao registrada")
        if not ref:
            raise ValidationError("transicao exige foto tipada registrada")

    def registrar_medicao(
        self,
        *,
        entidade: str,
        id_os: str,
        grandeza: str,
        valor: str,
        unidade: str,
        data: date | str,
        responsavel: str,
    ) -> dict:
        tag = validar_entidade(entidade)
        self.obter_os(id_os, entidade=tag)
        with session(self.db_path) as conn:
            id_medicao = _novo_id(conn, "medicoes", "id", f"MED-{tag}-")
            try:
                conn.execute(
                    """
                    INSERT INTO medicoes (
                        id, id_os, entidade, grandeza, valor, unidade, data, responsavel
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        id_medicao,
                        id_os,
                        tag,
                        texto_obrigatorio(grandeza, "grandeza"),
                        texto_obrigatorio(valor, "valor"),
                        texto_obrigatorio(unidade, "unidade"),
                        _data(data, "data"),
                        texto_obrigatorio(responsavel, "responsavel"),
                    ),
                )
            except sqlite3.IntegrityError as exc:
                raise traduzir_integrity(exc) from exc
            return _uma(conn, "SELECT * FROM medicoes WHERE id = ? AND entidade = ?", (id_medicao, tag))

    def listar_medicoes(self, entidade: str, id_os: str | None = None) -> list[dict]:
        tag = validar_entidade(entidade)
        sql = "SELECT * FROM medicoes WHERE entidade = ?"
        params: list[str] = [tag]
        if id_os:
            sql += " AND id_os = ?"
            params.append(id_os)
        sql += " ORDER BY id"
        with session(self.db_path) as conn:
            linhas = conn.execute(sql, params).fetchall()
        return [dict(linha) for linha in linhas]

    def registrar_foto_tipada(self, id_os: str, *, entidade: str, referencia: str) -> dict:
        atual = self.obter_os(id_os, entidade=entidade)
        if atual["status_os"] == "Faturado":
            raise TransitionError("OS faturada nao altera a foto tipada")
        ref = validar_ref_tipada(referencia)
        with session(self.db_path) as conn:
            conn.execute(
                """
                UPDATE ordens_servico
                SET ref_foto_tipada = ?
                WHERE id_os = ? AND entidade = ?
                """,
                (ref, id_os, atual["entidade"]),
            )
        return self.obter_os(id_os, entidade=entidade)

    def registrar_recebimento(
        self,
        *,
        entidade: str,
        id_os: str,
        data_recebimento: date | str,
        valor_recebido: float | str,
        forma: str,
        obs: str | None = None,
    ) -> dict:
        tag = validar_entidade(entidade)
        self.obter_os(id_os, entidade=tag)
        with session(self.db_path) as conn:
            id_recebimento = _novo_id(conn, "recebimentos", "id", f"REC-{tag}-")
            try:
                conn.execute(
                    """
                    INSERT INTO recebimentos (
                        id, id_os, entidade, data_recebimento, valor_recebido, forma, obs
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        id_recebimento,
                        id_os,
                        tag,
                        _data(data_recebimento, "data_recebimento"),
                        interpretar_recebido(valor_recebido),
                        texto_obrigatorio(forma, "forma"),
                        _opcional(obs),
                    ),
                )
            except sqlite3.IntegrityError as exc:
                raise traduzir_integrity(exc) from exc
            return _uma(
                conn,
                "SELECT * FROM recebimentos WHERE id = ? AND entidade = ?",
                (id_recebimento, tag),
            )

    def listar_recebimentos(self, entidade: str, id_os: str | None = None) -> list[dict]:
        tag = validar_entidade(entidade)
        sql = "SELECT * FROM recebimentos WHERE entidade = ?"
        params: list[str] = [tag]
        if id_os:
            sql += " AND id_os = ?"
            params.append(id_os)
        sql += " ORDER BY id"
        with session(self.db_path) as conn:
            linhas = conn.execute(sql, params).fetchall()
        return [dict(linha) for linha in linhas]

    def criar_backup(self, dest_dir: Path, *, tag: str, quando: date | None = None) -> Path:
        return criar_backup(self.db_path, Path(dest_dir), tag=tag, quando=quando)
