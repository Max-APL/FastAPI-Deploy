from fastapi import FastAPI
from mangum import Mangum

from datetime import date
from pydantic import BaseModel

from fastapi import Depends, HTTPException
from typing import List



class ClienteBaseModel(BaseModel):
    nombre: str
    apellido: str
    direccion: str
    telefono: str
    email: str
    fecha_nac: date
    sexo: str


class Cliente(ClienteBaseModel):
    cod_cli: str
    pass


# Simulación de una base de datos de clientes
fake_db_clientes = [
    {
        "cod_cli": "CLI001",
        "nombre": "Juan",
        "apellido": "Pérez",
        "direccion": "Av. Principal 123",
        "telefono": "555-1234",
        "email": "juan.perez@example.com",
        "fecha_nac": "1985-05-14",
        "sexo": "M"
    },
    {
        "cod_cli": "CLI002",
        "nombre": "María",
        "apellido": "Gómez",
        "direccion": "Calle Secundaria 456",
        "telefono": "555-5678",
        "email": "maria.gomez@example.com",
        "fecha_nac": "1990-08-22",
        "sexo": "F"
    },
    {
        "cod_cli": "CLI003",
        "nombre": "Carlos",
        "apellido": "López",
        "direccion": "Av. Central 789",
        "telefono": "555-8765",
        "email": "carlos.lopez@example.com",
        "fecha_nac": "1982-03-10",
        "sexo": "M"
    },
    {
        "cod_cli": "CLI004",
        "nombre": "Ana",
        "apellido": "Martínez",
        "direccion": "Calle Tercera 321",
        "telefono": "555-4321",
        "email": "ana.martinez@example.com",
        "fecha_nac": "1995-07-30",
        "sexo": "F"
    },
    {
        "cod_cli": "CLI005",
        "nombre": "Luis",
        "apellido": "García",
        "direccion": "Av. Cuarta 654",
        "telefono": "555-6543",
        "email": "luis.garcia@example.com",
        "fecha_nac": "1988-11-18",
        "sexo":"M"
    }
]

app = FastAPI()
handler = Mangum(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/client", response_model=List[Cliente])
async def obtener_clientes():
    print(fake_db_clientes)
    return [Cliente(**cliente) for cliente in fake_db_clientes]


@app.get("/client/{cliente_id}", response_model=Cliente)
async def obtener_cliente(cliente_id: str):
    cliente = next((cliente for cliente in fake_db_clientes if cliente["cod_cli"] == cliente_id), None)
    if cliente:
        response = Cliente(**cliente)
        return response
    raise HTTPException(status_code=404, detail="Cliente no encontrado")


@app.post("/crear", response_model=Cliente)
async def crear_cliente(cliente: Cliente):
    fake_db_clientes.append(cliente.dict())
    print("Agregado")
    print(fake_db_clientes)
    return cliente


@app.put("/actualizar/{cliente_id}", response_model=Cliente)
async def actualizar_cliente(cliente_id: str, cliente: ClienteBaseModel):
    for i, c in enumerate(fake_db_clientes):
        if c["cod_cli"] == cliente_id:
            cliente_update = Cliente(cod_cli=cliente_id, **cliente.dict())
            fake_db_clientes[i] = cliente_update.dict()
            return cliente_update
    raise HTTPException(status_code=404, detail="Cliente no encontrado")


@app.delete("/eliminar/{cliente_id}")
async def eliminar_cliente(cliente_id: str):
    for i, c in enumerate(fake_db_clientes):
        if c["cod_cli"] == cliente_id:
            del fake_db_clientes[i]
            return {"message": "Cliente eliminado"}
    raise HTTPException(status_code=404, detail="Cliente no encontrado")





