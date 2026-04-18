from beanie import Document
from pydantic import BaseModel
from typing import Optional
from beanie import PydanticObjectId
from datetime import datetime
from enum import Enum

class EstadoMarcacao(str, Enum):
    pendente = "pendente"
    confirmada = "confirmada"
    concluida = "concluida"
    cancelada = "cancelada"

class Marcacao(Document):
    clinica_id: PydanticObjectId
    servico_id: PydanticObjectId
    profissional_id: PydanticObjectId
    cliente_nome: str
    cliente_email: str
    cliente_telefone: str
    data: str
    slot: str
    estado: EstadoMarcacao = EstadoMarcacao.pendente
    taxa_paga: bool = False
    taxa_valor: float = 5.0
    qr_code: Optional[str] = None
    criada_em: datetime = datetime.utcnow()

    class Settings:
        name = "marcacoes"