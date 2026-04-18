from beanie import Document
from typing import Optional

class Clinica(Document):
    nome: str
    morada: str
    codigo_postal: str
    cidade: str
    telefone: Optional[str] = None
    telemovel: Optional[str] = None
    email: Optional[str] = None
    ativa: bool = True

    class Settings:
        name = "clinicas"