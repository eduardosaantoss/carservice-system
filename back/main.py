from fastapi import FastAPI
from pydantic import BaseModel

from database.database import Base, engine
from models.cliente import Cliente

app = FastAPI()

Base.metadata.create_all(bind=engine)

class Cliente(BaseModel):
    nome : str
    telefone : str
    email : str

@app.get("/")
def home():
    return {"CarService API - Funcionando"}

@app.get("/clientes")
def listar_clientes():
    return {"Lista de clientes"}

@app.post("/clientes")
def criar_cliente(cliente: Cliente):
    return cliente

