from beanie import Document
from typing import Optional
from beanie import PydanticObjectId

class Profissional(Document):
    nome: str
    especialidade: str
    clinica_id: PydanticObjectId
    ativo: bool = True

    class Settings:
        name = "profissionais"