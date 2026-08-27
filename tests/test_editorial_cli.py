"""CLI: pulse e Aprovar dry-run, sem publicar."""

from __future__ import annotations

from editorial.cli import main


def test_pulse_sem_token_usa_fixture(capsys, monkeypatch):
    monkeypatch.delenv("NOTION_TOKEN", raising=False)
    monkeypatch.setenv("CONFIRM", "0")
    assert main(["pulse"]) == 0
    out = capsys.readouterr().out
    assert "Por Status:" in out
    assert "Aguardando OK" in out
    assert "Editora" in out
    assert "Produtora" in out
    assert "Próximo Aguardando OK" in out
    assert "NUNCA publica" in out
    assert "Acervo" in out
    assert "AGT-09" in out  # menção de que NÃO há AGT-09
    assert "instagram.facebook" not in out.lower()


def test_aprovar_dry_run_nao_publica(capsys, monkeypatch):
    monkeypatch.delenv("NOTION_TOKEN", raising=False)
    monkeypatch.setenv("CONFIRM", "0")
    code = main(
        [
            "aprovar",
            "fixture-aguardando-ok",
            "--status",
            "Aguardando OK",
        ]
    )
    assert code == 0
    mixed = capsys.readouterr().out
    assert "Dry-run" in mixed
    assert "written=False" in mixed
    assert "published=False" in mixed
    assert "instagram=False" in mixed
    assert "n8n=False" in mixed
    assert "to_status=Aprovado" in mixed


def test_publicar_nao_e_comando(capsys):
    try:
        main(["publicar", "x"])
    except SystemExit as exc:
        assert exc.code != 0
    else:
        raise AssertionError("publicar não deveria ser um subcomando")


def test_recusar_sem_motivo_falha(capsys):
    try:
        main(["recusar", "fixture-aguardando-ok"])
    except SystemExit as exc:
        assert exc.code != 0
    else:
        raise AssertionError("recusar exige --reason")
