from pydantic import BaseModel, Field
from typing import Optional

class ItemVentaCreate(BaseModel):
    producto_id: str = Field(..., example="66b9f44f5e5e13b3b6a7c213")
    nombre: str = Field(..., example="Gaseosa Coca Cola 2L")
    precio_unitario: float = Field(..., gt=0, example=1200.50)
    cantidad: int = Field(..., gt=0, example=2)
    subtotal: float = Field(..., gt=0, example=2401.00)

class ItemVentaUpdate(BaseModel):
    nombre: Optional[str] = Field(None)
    precio_unitario: Optional[float] = Field(None, gt=0)
    cantidad: Optional[int] = Field(None, gt=0)
    subtotal: Optional[float] = Field(None, gt=0)

class ItemVentaResponse(ItemVentaCreate):
    id: str = Field(..., alias="_id")

    model_config = {
        "populate_by_name": True
    }