from fastapi import APIRouter, Depends, HTTPException
from typing import List

from clientSquema import Cliente, ClienteBaseModel, fake_db_clientes

router = APIRouter()

@router.get("/all", response_model=List[Cliente])
async def obtener_clientes():
    print(fake_db_clientes)
    return [Cliente(**cliente) for cliente in fake_db_clientes]


@router.get("/{cliente_id}", response_model=Cliente)
async def obtener_cliente(cliente_id: str):
    cliente = next((cliente for cliente in fake_db_clientes if cliente["cod_cli"] == cliente_id), None)
    if cliente:
        response = Cliente(**cliente)
        return response
    raise HTTPException(status_code=404, detail="Cliente no encontrado")


@router.post("/crear", response_model=Cliente)
async def crear_cliente(cliente: Cliente):
    fake_db_clientes.append(cliente.dict())
    print("Agregado")
    print(fake_db_clientes)
    return cliente


@router.put("/actualizar/{cliente_id}", response_model=Cliente)
async def actualizar_cliente(cliente_id: str, cliente: ClienteBaseModel):
    for i, c in enumerate(fake_db_clientes):
        if c["cod_cli"] == cliente_id:
            cliente_update = Cliente(cod_cli=cliente_id, **cliente.dict())
            fake_db_clientes[i] = cliente_update.dict()
            return cliente_update
    raise HTTPException(status_code=404, detail="Cliente no encontrado")


@router.delete("/eliminar/{cliente_id}")
async def eliminar_cliente(cliente_id: str):
    for i, c in enumerate(fake_db_clientes):
        if c["cod_cli"] == cliente_id:
            del fake_db_clientes[i]
            return {"message": "Cliente eliminado"}
    raise HTTPException(status_code=404, detail="Cliente no encontrado")