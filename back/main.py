from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from database.database import Base, engine, get_db
from models.cliente import Cliente

app = FastAPI()

Base.metadata.create_all(bind=engine)


class ClienteCreate(BaseModel):
    nome: str
    telefone: str
    email: str


class ClienteResponse(ClienteCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


@app.get("/")
def home():
    return {"message": "AutoCare API funcionando!"}


@app.get("/clientes", response_model=list[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()

@app.get("/clientes/{cliente_id}", response_model=ClienteResponse)
def buscar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    return cliente

@app.post("/clientes", response_model=ClienteResponse)
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    novo_cliente = Cliente(
        nome=cliente.nome,
        telefone=cliente.telefone,
        email=cliente.email,
    )
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return novo_cliente

@app.put("/clientes/{cliente_id}", response_model=ClienteResponse)
def atualizar_cliente(cliente_id: int, dados: ClienteCreate, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    cliente.nome = dados.nome
    cliente.telefone = dados.telefone
    cliente.email = dados.email

    db.commit()
    db.refresh(cliente)
    return cliente

@app.delete("/clientes/{cliente_id}")
def deletar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    db.delete(cliente)
    db.commit()
    return {"mensagem": "Cliente deletado com sucesso"}