from pydantic import BaseModel
from datetime import datetime

class InvoiceLineCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class InvoiceCreate(BaseModel):
    customer_id: int
    lines: list[InvoiceLineCreate]

class InvoiceLine(InvoiceLineCreate):
    id: int

    class Config:
       from_attributes = True

class Invoice(InvoiceCreate):
    id: int
    created_at: datetime
    lines: list[InvoiceLine]

    class Config:
        from_attributes = True

