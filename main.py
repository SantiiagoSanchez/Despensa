from fastapi import FastAPI, Request
from routers import productos
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from bd.client import db



app = FastAPI()

# 1. Configurar templates
templates = Jinja2Templates(directory="templates")

# 2. Ruta HTML antes del router
@app.get("/productos/lista")
def lista_prod(request: Request):
    productos_list = list(db.productos.find())
    for p in productos_list:
        p["_id"] = str(p["_id"])
    return templates.TemplateResponse(
        "producto/lista.html",
        {"request": request, "productos": productos_list}
    )

# 3. Incluir router después
app.include_router(productos.router)

