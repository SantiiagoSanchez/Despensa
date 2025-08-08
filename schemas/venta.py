from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from schemas.itemventa import ItemVentaCreate

class VentaCreate(BaseModel):
    cliente: Optional[str] = Field("Consumidor final", example="Juan Perez")
    total: float = Field(..., ge=0, example=2401.00)
    items: List[ItemVentaCreate] = Field(..., min_length=1)

class VentaUpdate(BaseModel):
    cliente: Optional[str] = Field(None)
    total: Optional[float] = Field(None, ge=0)
    items: Optional[List[ItemVentaCreate]] = None

class VentaResponse(VentaCreate):
    id: str = Field(..., alias="_id")
    fecha: Optional[datetime] = Field(None, example="2025-08-08T12:34:56")

    model_config = {
        "populate_by_name": True
    }