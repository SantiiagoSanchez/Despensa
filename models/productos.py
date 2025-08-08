from pydantic import BaseModel, Field
from typing import Optional

class Producto(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    nombre: str = Field(..., example="Gaseosa Coca Cola 2L")
    descripcion: Optional[str] = Field(None, example="Botella de plástico retornable")
    precio: float = Field(..., gt=0, example=1200.50)
    stock: int = Field(0, ge=0, example=50)
    activo: bool = Field(True, example=True)

    model_config = {
        "populate_by_name": True
    }


#field(...) con ... para obligatorio
#alias="_id" para que Pydantic entienda que el campo Mongo _id se mapea a id en Python
#model_config con "populate_by_name": True para que funcione bien con alias
#Validaciones extra como gt=0 o ge=0 para números positivos