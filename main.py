from fastapi import FastAPI
from routers import productos 
app = FastAPI()


app.include_router(productos.router)

@app.get("/")
async def Index() -> dict[str, str]:
    return {"Hola": "Mundo"}

@app.get("/about")
async def About() -> str:
    return "Esto es una pagina inicial para verificar que todo funcione"