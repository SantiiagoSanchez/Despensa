from pydantic import BaseModel, Field
from typing import Optional

class ProductoCreate(BaseModel):
    nombre: str = Field(..., example="Gaseosa Coca Cola 2L")
    descripcion: Optional[str] = Field(None, example="Botella retornable")
    precio: float = Field(..., gt=0, example=1200.50)
    stock: int = Field(0, ge=0, example=50)
    activo: bool = Field(True, example=True)

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None)
    descripcion: Optional[str] = Field(None)
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    activo: Optional[bool] = Field(None)

class ProductoResponse(ProductoCreate):
    id: str = Field(..., alias="_id")

    model_config = {
        "populate_by_name": True
    }