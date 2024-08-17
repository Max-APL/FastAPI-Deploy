from fastapi import FastAPI
from mangum import Mangum

from router import clientRouter

app = FastAPI()
handler = Mangum(app)

app.include_router(clientRouter.router, prefix="/client", tags=["client"])

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}








