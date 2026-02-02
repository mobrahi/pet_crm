# backend/schemas.py
from pydantic import BaseModel
from typing import List
from datetime import datetime
from enum import Enum

# ---------- Customer ----------
class CustomerBase(BaseModel):
    name: str
    email: str

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    class Config:
        from_attributes = True


# ---------- Product ----------
class ProductBase(BaseModel):
    name: str
    price: float
    stock: int
    reorder_level: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    supplier_id: int | None
    class Config:
        from_attributes = True

# ---------- Supplier ----------
class SupplierBase(BaseModel):
    name: str
    contact_email: str
    phone: str

class SupplierCreate(SupplierBase):
    pass

class Supplier(SupplierBase):
    id: int
    class Config:
        from_attributes = True

# ---------- Invoice ----------
class InvoiceBase(BaseModel):
    amount: float
    customer_id: int
    product_id: int

class InvoiceCreate(InvoiceBase):
    pass

class Invoice(InvoiceBase):
    id: int
    date: datetime
    class Config:
        from_attributes = True
        
# ---------- Purchase Order ----------
class POStatus(str, Enum):
    draft = "draft"
    submitted = "submitted"
    approved = "approved"
    fulfilled = "fulfilled"
    closed = "closed"
    cancelled = "cancelled"

class PurchaseOrderLineBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class PurchaseOrderLineCreate(PurchaseOrderLineBase):
    pass

class PurchaseOrderLine(PurchaseOrderLineBase):
    id: int
    class Config:
        from_attributes = True

class PurchaseOrderBase(BaseModel):
    supplier_id: int
    status: POStatus = POStatus.draft

class PurchaseOrderCreate(PurchaseOrderBase):
    lines: List[PurchaseOrderLineCreate]

class PurchaseOrder(PurchaseOrderBase):
    id: int
    created_at: datetime
    lines: List[PurchaseOrderLine]
    class Config:
        from_attributes = True
