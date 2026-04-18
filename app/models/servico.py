from beanie import Document
from pydantic import BaseModel
from typing import Optional
from enum import Enum

class CategoriaServico(str, Enum):
    consulta = "consulta"
    tratamento = "tratamento"

class Servico(Document):
    nome: str
    categoria: CategoriaServico
    duracao_min: int
    preco_base: float
    ativo: bool = True

    class Settings:
        name = "servicos"