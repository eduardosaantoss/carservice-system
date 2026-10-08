from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    veiculos = relationship("Veiculo", back_populates="cliente", cascade="all, delete-orphan")