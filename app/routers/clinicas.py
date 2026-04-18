from fastapi import APIRouter
from app.models.clinica import Clinica

router = APIRouter()

@router.get("/")
async def get_clinicas():
    clinicas = await Clinica.find_all().to_list()
    return clinicas

@router.post("/")
async def criar_clinica(clinica: Clinica):
    await clinica.insert()
    return clinica