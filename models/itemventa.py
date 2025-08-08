from pydantic import BaseModel, Field
from typing import Optional

class ItemVenta(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    producto_id: str = Field(..., example="66b9f44f5e5e13b3b6a7c213")
    nombre: str = Field(..., example="Gaseosa Coca Cola 2L")
    precio_unitario: float = Field(..., gt=0, example=1200.50)
    cantidad: int = Field(..., gt=0, example=2)
    subtotal: float = Field(..., gt=0, example=2401.00)

    model_config = {
        "populate_by_name": True
    }

