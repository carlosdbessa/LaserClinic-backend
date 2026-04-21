from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.auth import hash_password, verify_password, create_token
from app.models.cliente import Cliente
import resend
import random
import os
from datetime import datetime, timedelta

router = APIRouter()


class RegistoInput(BaseModel):
    nome: str
    email: str
    telefone: str
    password: str


class LoginInput(BaseModel):
    email: str
    password: str


class RecuperarInput(BaseModel):
    email: str


class RedefinirInput(BaseModel):
    email: str
    codigo: str
    nova_password: str


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
    cliente = await Cliente.find_one({"email": dados.email})
    if not cliente:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    if not verify_password(dados.password, cliente.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = create_token(dados.email)
    return {"token": token, "cliente": {"nome": cliente.nome, "email": cliente.email, "telefone": cliente.telefone}}


@router.post("/recuperar")
async def recuperar_password(dados: RecuperarInput):
    print("Email recebido:", dados.email)
    cliente = await Cliente.find_one({"email": dados.email})
    print("Cliente encontrado:", cliente)
    if not cliente:
        return {"mensagem": "Se o email existir, receberás um código"}
    codigo = str(random.randint(100000, 999999))
    expira = datetime.utcnow() + timedelta(minutes=15)
    cliente.codigo_recuperacao = codigo
    cliente.codigo_expira = expira
    await cliente.save()
    resend.api_key = os.getenv("RESEND_API_KEY")
    print("A enviar email para:", dados.email)
    print("API Key:", os.getenv("RESEND_API_KEY"))
    resend.Emails.send({
        "from": "LaserClinic <noreply@resend.dev>",
        "to": dados.email,
        "subject": "Recuperação de password",
        "html": f"""
            <h2>Recuperação de password</h2>
            <p>O teu código de recuperação é:</p>
            <h1 style="color: #7d2040; letter-spacing: 8px;">{codigo}</h1>
            <p>Este código expira em 15 minutos.</p>
            <p>Se não pediste a recuperação, ignora este email.</p>
        """
    })
    return {"mensagem": "Se o email existir, receberás um código"}


@router.post("/redefinir")
async def redefinir_password(dados: RedefinirInput):
    cliente = await Cliente.find_one({"email": dados.email})
    if not cliente:
        raise HTTPException(status_code=400, detail="Código inválido")
    if cliente.codigo_recuperacao != dados.codigo:
        raise HTTPException(status_code=400, detail="Código inválido")
    if datetime.utcnow() > cliente.codigo_expira:
        raise HTTPException(status_code=400, detail="Código expirado")
    cliente.password_hash = hash_password(dados.nova_password)
    cliente.codigo_recuperacao = None
    cliente.codigo_expira = None
    await cliente.save()
    return {"mensagem": "Password alterada com sucesso"}