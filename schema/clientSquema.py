from datetime import date
from pydantic import BaseModel



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