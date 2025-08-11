from fastapi import FastAPI, Request, Form
from routers import productos
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from bd.client import db



app = FastAPI()


#fastapi dev main.py Arrancar servidor


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

@app.get("/productos/nuevo")
def nuevo_producto(request: Request):
    return templates.TemplateResponse("producto/nuevo.html", {"request": request})

@app.post("/productos")
def crear_producto(
    request: Request,
    nombre: str = Form(...),
    descripcion: str = Form(None),
    precio: float = Form(...),
    stock: int = Form(...),
    activo: bool = Form(False)
):
    nuevo = {
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": precio,
        "stock": stock,
        "activo": activo,
    }
    db.productos.insert_one(nuevo)
    return RedirectResponse(url="/productos/lista", status_code=303)

# 3. Incluir router después
app.include_router(productos.router)

