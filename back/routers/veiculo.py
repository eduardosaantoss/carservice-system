from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database.database import get_db
from models.cliente import Cliente
from models.veiculos import Veiculo
from schemas.veiculo import VeiculoCreate, VeiculoResponse

router = APIRouter(prefix="/veiculos", tags=["veiculos"])

def veiculo_erro404(veiculo_id: int, db: Session) -> Veiculo:
    veiculo = db.query(Veiculo).filter(Veiculo.id == veiculo_id).first()
    if veiculo is None:
        raise HTTPException(status_code=404, detail="Veiculo não encontrado no banco de dados")
    return veiculo


