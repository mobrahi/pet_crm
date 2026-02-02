from pydantic import BaseModel
from datetime import datetime
from backend.models.purchase_orders import POStatus

class PurchaseOrderLineCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class PurchaseOrderCreate(BaseModel):
    supplier_id: int
    status: POStatus = POStatus.draft
    lines: list[PurchaseOrderLineCreate]

class PurchaseOrderLine(PurchaseOrderLineCreate):
    id: int

    class Config:
        from_attributes = True

class PurchaseOrder(PurchaseOrderCreate):
    id: int
    created_at: datetime
    lines: list[PurchaseOrderLine]

    class Config:
        from_attributes = True
