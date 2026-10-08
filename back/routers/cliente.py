from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database.database import get_db
from models.cliente import Cliente
from schemas.cliente import ClienteCreate, ClienteResponse

router = APIRouter(prefix="/clientes", tags=["clientes"])

def erro404(cliente_id: int, db: Session) -> Cliente:
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    return cliente


@router.get("", response_model=list[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()


@router.get("/{cliente_id}", response_model=ClienteResponse)
def buscar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return erro404(cliente_id, db)


@router.post("", response_model=ClienteResponse)
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    novo_cliente = Cliente(
        nome=cliente.nome,
        telefone=cliente.telefone,
        email=cliente.email,
    )
    db.add(novo_cliente)
    try:
        db.commit()
        db.refresh(novo_cliente)
        return novo_cliente
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email já cadastrado!")


@router.put("/{cliente_id}", response_model=ClienteResponse)
def atualizar_cliente(
    cliente_id: int, dados: ClienteCreate, db: Session = Depends(get_db)
):
    cliente = erro404(cliente_id, db)

    cliente.nome = dados.nome
    cliente.telefone = dados.telefone
    cliente.email = dados.email

    try:
        db.commit()
        db.refresh(cliente)
        return cliente
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email já cadastrado!")


@router.delete("/{cliente_id}")
def deletar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = erro404(cliente_id, db)

    db.delete(cliente)
    db.commit()
    return {"mensagem": "Cliente deletado com sucesso"}