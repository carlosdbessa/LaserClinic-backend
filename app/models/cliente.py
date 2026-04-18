from beanie import Document
from typing import Optional

class Cliente(Document):
    nome: str
    email: str
    telefone: str
    password_hash: str
    ativo: bool = True

    class Settings:
        name = "clientes"