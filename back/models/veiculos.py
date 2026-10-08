from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import base

class Veiculo(base):
    __tablemame__ = "veiculos"

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    placa = Column(String, unique=True, index=True, nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False)
    
    # Passamos "Cliente" como string para evitar importação circular
    cliente = relationship("Cliente", back_populates="veiculos")