from beanie import Document
from pydantic import BaseModel
from typing import Optional

class Clinica(Document):
    nome: str
    morada: str
    cidade: str
    telefone: Optional[str] = None
    ativa: bool = True

    class Settings:
        name = "clinicas"