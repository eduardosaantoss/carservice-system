from fastapi import Depends, FastAPI, HTTPException


from database.database import Base, engine, get_db
from models.cliente import Cliente
from routers.cliente import router as clientes_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(clientes_router)

