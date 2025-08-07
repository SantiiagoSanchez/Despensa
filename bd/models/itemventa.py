from pydantic import BaseModel

class ItemVenta(BaseModel):
    id: str | None = None
    producto_id: str
    nombre: str
    precio_unitario: float
    cantidad: int
    subtotal: float

