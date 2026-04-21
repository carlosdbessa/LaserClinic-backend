from beanie import Document
from typing import Optional
from datetime import datetime

class Cliente(Document):
    nome: str
    email: str
    telefone: str
    password_hash: str
    ativo: bool = True
    codigo_recuperacao: Optional[str] = None
    codigo_expira: Optional[datetime] = None

    class Settings:
        name = "clientes"