from pydantic import BaseModel

class SupplierCreate(BaseModel):
    name: str
    contact_email: str | None = None
    phone: str | None = None

class Supplier(SupplierCreate):
    id: int

    class Config:
        from_attributes = True
