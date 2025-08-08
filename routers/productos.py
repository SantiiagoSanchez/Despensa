from fastapi import APIRouter, HTTPException
from bson import ObjectId
from bd.client import db
from models.productos import Producto
from schemas.productos import ProductoCreate, ProductoUpdate, ProductoResponse

router = APIRouter(prefix="/productos", tags=["Productos"])

def convertir_id(producto):
    if producto:
        producto["_id"] = str(producto["_id"])
    return producto

# Obtener todos los productos
@router.get("/", response_model=list[ProductoResponse])
def listar_productos():
    productos = list(db.productos.find())
    return [convertir_id(p) for p in productos]

# Obtener un producto por ID
@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: str):
    producto = db.productos.find_one({"_id": ObjectId(producto_id)})
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return convertir_id(producto)

# Crear producto
@router.post("/", response_model=ProductoResponse)
def crear_producto(producto: ProductoCreate):
    nuevo = dict(producto)
    resultado = db.productos.insert_one(nuevo)
    producto_creado = db.productos.find_one({"_id": resultado.inserted_id})
    return convertir_id(producto_creado)

# Actualizar producto
@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(producto_id: str, producto: ProductoUpdate):
    actualizado = db.productos.find_one_and_update(
        {"_id": ObjectId(producto_id)},
        {"$set": {k: v for k, v in producto.dict().items() if v is not None}},
        return_document=True
    )
    if not actualizado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return convertir_id(actualizado)

# Eliminar producto
@router.delete("/{producto_id}")
def eliminar_producto(producto_id: str):
    eliminado = db.productos.find_one_and_delete({"_id": ObjectId(producto_id)})
    if not eliminado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto eliminado correctamente"}