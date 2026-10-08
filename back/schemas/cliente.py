from pydantic import BaseModel, ConfigDict

class ClienteCreate(BaseModel):
    nome : str
    telefone : str
    email : str

class ClienteResponse(ClienteCreate):
    id : int

    model_config = ConfigDict(from_attributes=True)