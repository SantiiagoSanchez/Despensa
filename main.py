from fastapi import FastAPI, Request, Form, HTTPException, status
from bson import ObjectId
from routers import productos
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from bd.client import db
from datetime import datetime



app = FastAPI()


#fastapi dev main.py Arrancar servidor


# 1. Configurar templates
templates = Jinja2Templates(directory="templates")

# 2. CRUD DE PRODUCTOS
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

@app.get("/productos/{id}/editar")
def editar_producto(request: Request, id: str):
    producto = db.productos.find_one({"_id": ObjectId(id)})
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto["_id"] = str(producto["_id"])
    return templates.TemplateResponse("producto/editar.html", {"request": request, "producto": producto})

@app.post("/productos/{id}")
def actualizar_producto(
    request: Request,
    id: str,
    nombre: str = Form(...),
    descripcion: str = Form(None),
    precio: float = Form(...),
    stock: int = Form(...),
    activo: bool = Form(False)
):
    actualizacion = {
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": precio,
        "stock": stock,
        "activo": activo,
    }
    result = db.productos.update_one({"_id": ObjectId(id)}, {"$set": actualizacion})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado para actualizar")
    return RedirectResponse(url="/productos/lista", status_code=303)

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

@app.post("/productos/{id}/eliminar")
def eliminar_producto(id: str):
    result = db.productos.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return RedirectResponse(url="/productos/lista", status_code=status.HTTP_303_SEE_OTHER)
# 3. AREA DE VENTAS

@app.get("/ventas/nuevo")
def nueva_venta(request: Request):
    productos = list(db.productos.find({"activo": True, "stock": {"$gt": 0}}))
    for p in productos:
        p["_id"] = str(p["_id"])
    return templates.TemplateResponse("venta/nuevo.html", {"request": request, "productos": productos})
app.include_router(productos.router)

@app.post("/ventas")
def crear_venta(
    request: Request,
    producto_id: str = Form(...),
    cantidad: int = Form(...)
):
    producto = db.productos.find_one({"_id": ObjectId(producto_id)})

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if producto["stock"] < cantidad:
        raise HTTPException(status_code=400, detail="Stock insuficiente")

    precio_unitario = producto["precio"]
    subtotal = precio_unitario * cantidad
    total = subtotal

    item = {
        "producto_id": producto_id,
        "nombre": producto["nombre"],
        "precio_unitario": precio_unitario,
        "cantidad": cantidad,
        "subtotal": subtotal
    }

    venta = {
        "fecha": datetime.now(),
        "items": [item],
        "total": total
    }

    db.ventas.insert_one(venta)

    # Descontar stock
    db.productos.update_one(
        {"_id": ObjectId(producto_id)},
        {"$inc": {"stock": -cantidad}}
    )

    return RedirectResponse(url="/productos/lista", status_code=303)

@app.get("/historial/ventas")
def lista_ventas(request: Request):
    ventas = list(db.ventas.find())
    for venta in ventas:
        venta["_id"] = str(venta["_id"])
        venta["id"] = venta["_id"]  
    return templates.TemplateResponse(
        "venta/lista.html",
        {"request": request, "ventas": ventas}
    )

