from pydantic import BaseModel, ConfigDict, Field, field_validator

class VeiculoBase(BaseModel):
    marca : str
    modelo : str
    placa : str
    cliente_id : int

    @field_validator("placa")
    @classmethod
    def forma_placa(cls, valor: str) -> str:
        placa_formatada = valor.strip().upper().replace("-", "")
        if len(placa_formatada) != 7:
            raise ValueError("A placa deve conter 7 digitos.")
        pass

class VeiculoCreate(VeiculoBase):
    pass

class VeiculoResponse(VeiculoCreate):
    id : int

    model_config = ConfigDict(from_attributes=True)

