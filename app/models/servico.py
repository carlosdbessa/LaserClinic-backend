from beanie import Document
from enum import Enum

class CategoriaServico(str, Enum):
    consulta = "consulta"
    tratamento = "tratamento"

class Servico(Document):
    nome: str
    categoria: CategoriaServico
    ativo: bool = True

    class Settings:
        name = "servicos"