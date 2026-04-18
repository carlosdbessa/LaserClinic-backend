from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.auth import hash_password, verify_password, create_token
from app.models.cliente import Cliente

router = APIRouter()

class RegistoInput(BaseModel):
    nome: str
    email: str
    telefone: str
    password: str

class LoginInput(BaseModel):
    email: str
    password: str

@router.post("/registo")
async def registo(dados: RegistoInput):
    existente = await Cliente.find_one({"email": dados.email})
    if existente:
        raise HTTPException(status_code=400, detail="Email já registado")
    
    cliente = Cliente(
        nome=dados.nome,
        email=dados.email,
        telefone=dados.telefone,
        password_hash=hash_password(dados.password),
    )
    await cliente.insert()
    
    token = create_token(dados.email)
    return {"token": token, "cliente": {"nome": cliente.nome, "email": cliente.email}}

@router.post("/login")
async def login(dados: LoginInput):
    cliente = await Cliente.find_one(Cliente.email == dados.email)
    if not cliente:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    if not verify_password(dados.password, cliente.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    token = create_token(dados.email)
    return {"token": token, "cliente": {"nome": cliente.nome, "email": cliente.email, "telefone": cliente.telefone}}