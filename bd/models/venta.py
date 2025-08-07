from pydantic import BaseModel
from datetime import datetime
from models.itemventa import ItemVenta


class Venta(BaseModel):
    id: str | None = None   
    cliente: str | None = "Consumidor final"
    fecha: datetime | None = None
    total: float
    items: list[ItemVenta]