from pydantic import BaseModel, Field
from typing import Optional

class ItemVentaCreate(BaseModel):
    producto_id: str = Field(..., example="66b9f44f5e5e13b3b6a7c213")
    cantidad: int = Field(..., gt=0, example=2)


class ItemVentaResponse(BaseModel):
    producto_id: str
    nombre: str
    precio_unitario: float
    cantidad: int
    subtotal: float
    id: Optional[str] = Field(None, alias="_id")

    model_config = {
        "populate_by_name": True
    }