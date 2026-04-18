from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import init_db
from .models.clinica import Clinica
from .models.servico import Servico
from .models.profissional import Profissional
from .models.marcacao import Marcacao
from .routers import clinicas, servicos, marcacoes

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db([Clinica, Servico, Profissional, Marcacao])
    yield

app = FastAPI(
    title="LaserClinic API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(clinicas.router, prefix="/clinicas", tags=["Clínicas"])
app.include_router(servicos.router, prefix="/servicos", tags=["Serviços"])
app.include_router(marcacoes.router, prefix="/marcacoes", tags=["Marcações"])

@app.get("/")
async def root():
    return {"message": "LaserClinic API está online"}