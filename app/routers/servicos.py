from fastapi import APIRouter
from app.models.servico import Servico

router = APIRouter()

@router.get("/")
async def get_servicos():
    servicos = await Servico.find_all().to_list()
    return servicos

@router.post("/")
async def criar_servico(servico: Servico):
    await servico.insert()
    return servico