from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int = 0
    reorder_level: int = 10
    supplier_id: int

class Product(ProductCreate):
    id: int

    class Config:
        from_attributes = True