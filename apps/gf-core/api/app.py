"""API local. Não publica, não chama n8n e não grava planilha remota."""

from __future__ import annotations

import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, Query, Request
from fastapi.responses import JSONResponse, Response

from api.schemas import BackupIn, ClienteIn, Entidade, EquipamentoIn, OsIn, TransicaoIn
from core.errors import EntityIsolationError, GfCoreError, NotFoundError
from db.connection import default_db_path, init_db
from db.repository import GfRepository

router = APIRouter()


def _repo(request: Request) -> GfRepository:
    return GfRepository(request.app.state.db_path)


def _erro(exc: GfCoreError) -> JSONResponse:
    codigo = 400
    if isinstance(exc, NotFoundError):
        codigo = 404
    elif isinstance(exc, EntityIsolationError):
        codigo = 409
    return JSONResponse(status_code=codigo, content={"erro": type(exc).__name__, "mensagem": str(exc)})


@router.get("/health")
def health() -> dict:
    return {"app": "gf-core", "modo": "local", "publicado": False, "n8n": False, "hotmart": False}


@router.post("/clientes")
def post_cliente(payload: ClienteIn, request: Request) -> dict:
    return _repo(request).criar_cliente(**payload.model_dump())


@router.get("/clientes")
def get_clientes(request: Request, entidade: Entidade = Query(...)) -> dict:
    return {"entidade": entidade, "itens": _repo(request).listar_clientes(entidade)}


@router.post("/equipamentos")
def post_equipamento(payload: EquipamentoIn, request: Request) -> dict:
    dados = payload.model_dump()
    quando = dados.pop("data_referencia")
    return _repo(request).criar_equipamento(**dados, quando=quando)


@router.get("/equipamentos")
def get_equipamentos(request: Request, entidade: Entidade = Query(...)) -> dict:
    return {"entidade": entidade, "itens": _repo(request).listar_equipamentos(entidade)}


@router.post("/ordens")
def post_os(payload: OsIn, request: Request) -> dict:
    return _repo(request).abrir_os(**payload.model_dump())


@router.get("/ordens")
def get_ordens(request: Request, entidade: Entidade = Query(...), status_os: str | None = None) -> dict:
    return {"entidade": entidade, "itens": _repo(request).listar_os(entidade, status_os)}


@router.get("/ordens/{id_os}")
def get_os(id_os: str, request: Request, entidade: Entidade = Query(...)) -> dict:
    return _repo(request).obter_os(id_os, entidade=entidade)


@router.post("/ordens/{id_os}/transicao")
def post_transicao(
    id_os: str,
    payload: TransicaoIn,
    request: Request,
    entidade: Entidade = Query(...),
) -> dict:
    return _repo(request).transicionar_os(
        id_os,
        payload.status_destino,
        entidade=entidade,
        quando=payload.quando,
    )


@router.get("/export/centros.csv")
def get_centros(request: Request, entidade: Entidade = Query(...)) -> Response:
    corpo = _repo(request).exportar_csv_centros(entidade)
    return Response(content=corpo, media_type="text/csv; charset=utf-8")


@router.get("/export/heros.csv")
def get_heros(request: Request, entidade: Entidade = Query(...)) -> Response:
    corpo = _repo(request).exportar_csv_heros(entidade)
    return Response(content=corpo, media_type="text/csv; charset=utf-8")


@router.get("/export/consolidado.csv")
def get_consolidado(
    request: Request,
    entidade: Entidade = Query(...),
    anomes: str | None = None,
) -> Response:
    corpo = _repo(request).exportar_csv_consolidado(entidade, anomes)
    return Response(content=corpo, media_type="text/csv; charset=utf-8")


@router.post("/backup")
def post_backup(payload: BackupIn, request: Request) -> dict:
    destino = Path(getattr(request.app.state, "backup_dir", APP_ROOT / "backups"))
    arquivo = _repo(request).criar_backup(destino, tag=payload.tag, quando=payload.quando)
    return {"nome": arquivo.name, "arquivo": arquivo.name}


def create_app(db_path: Path | None = None, backup_dir: Path | None = None) -> FastAPI:
    @asynccontextmanager
    async def _vida(app: FastAPI):
        init_db(app.state.db_path)
        yield

    app = FastAPI(
        title="gf-core",
        summary="OS local da Holding Grupo Fidalgo. Unpublished.",
        lifespan=_vida,
    )
    app.state.db_path = Path(db_path) if db_path else default_db_path()
    app.state.backup_dir = Path(backup_dir) if backup_dir else APP_ROOT / "backups"
    app.include_router(router)
    app.add_exception_handler(GfCoreError, lambda _request, exc: _erro(exc))
    return app


app = create_app()
