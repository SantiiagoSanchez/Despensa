from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from models.itemventa import ItemVenta


class Venta(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    cliente: Optional[str] = Field("Consumidor final", example="Juan Perez")
    fecha: Optional[datetime] = Field(None, example="2025-08-08T12:34:56")
    total: float = Field(..., ge=0, example=2401.00)
    items: list[ItemVenta] = Field(..., min_length=1)

    model_config = {
        "populate_by_name": True
    }