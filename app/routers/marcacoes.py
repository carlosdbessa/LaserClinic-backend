from fastapi import APIRouter
from app.models.marcacao import Marcacao
import uuid

router = APIRouter()

@router.get("/")
async def get_marcacoes():
    marcacoes = await Marcacao.find_all().to_list()
    return marcacoes

@router.post("/")
async def criar_marcacao(marcacao: Marcacao):
    marcacao.qr_code = str(uuid.uuid4())[:8].upper()
    await marcacao.insert()
    return marcacao

@router.get("/{marcacao_id}")
async def get_marcacao(marcacao_id: str):
    marcacao = await Marcacao.get(marcacao_id)
    return marcacao

@router.patch("/{marcacao_id}/estado")
async def atualizar_estado(marcacao_id: str, estado: str):
    marcacao = await Marcacao.get(marcacao_id)
    marcacao.estado = estado
    await marcacao.save()
    return marcacao