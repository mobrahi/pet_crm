from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from backend.database import Base
from datetime import datetime
import enum

# -------------------
# Enum for PO Status
# -------------------
class POStatus(enum.Enum):
    draft = "draft"
    submitted = "submitted"
    approved = "approved"
    fulfilled = "fulfilled"
    closed = "closed"
    cancelled = "cancelled"

# -------------------
# Purchase Order Header
# -------------------
class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    status = Column(Enum(POStatus), default=POStatus.draft)
    created_at = Column(DateTime, default=datetime.utcnow)

    supplier = relationship("Supplier", back_populates="purchase_orders")
    lines = relationship(
        "PurchaseOrderLine",
        back_populates="purchase_order",
        cascade="all, delete-orphan"
    )

# -------------------
# Purchase Order Line Items
# -------------------
class PurchaseOrderLine(Base):
    __tablename__ = "purchase_order_lines"

    id = Column(Integer, primary_key=True, index=True)
    purchase_order_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    purchase_order = relationship("PurchaseOrder", back_populates="lines")
    product = relationship("Product", back_populates="purchase_order_lines")
