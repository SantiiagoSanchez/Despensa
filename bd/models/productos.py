from pydantic import BaseModel

class Producto(BaseModel):
    id: str | None = None #Id opcional (MongoDB lo genera solo)
    nombre: str  #Nombre obligatorio
    descripcion: str| None = None #Descripcion opcional
    precio: float #Precio obligatorio
    stock: int= 0   #Stock con valor por defecto en 0
    activo: bool = True #Producto activo por defecto