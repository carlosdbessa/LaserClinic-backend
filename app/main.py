from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import init_db
from .models.clinica import Clinica
from .models.servico import Servico
from .models.profissional import Profissional
from .models.marcacao import Marcacao
from .routers import clinicas, servicos, marcacoes
from .routers import clinicas, servicos, marcacoes, auth
from .models.cliente import Cliente

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db([Clinica, Servico, Profissional, Marcacao, Cliente])
    yield

app = FastAPI(
    title="LaserClinic API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(clinicas.router, prefix="/clinicas", tags=["Clínicas"])
app.include_router(servicos.router, prefix="/servicos", tags=["Serviços"])
app.include_router(marcacoes.router, prefix="/marcacoes", tags=["Marcações"])
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])

@app.get("/")
async def root():
    return {"message": "LaserClinic API está online"}