from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Invoice, InvoiceLine, Product
from backend.schemas import InvoiceCreate, Invoice

router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.post("/", response_model=Invoice)
def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    # Create invoice header
    new_invoice = Invoice(customer_id=invoice.customer_id)
    db.add(new_invoice)
    db.flush()  # ensures new_invoice.id is available

    # Add line items
    total_amount = 0
    for line in invoice.lines:
        product = db.query(Product).filter(Product.id == line.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {line.product_id} not found")

        line_total = line.quantity * line.unit_price
        total_amount += line_total

        db.add(InvoiceLine(invoice_id=new_invoice.id, **line.dict()))

    # Optionally persist total_amount in Invoice if you have a column for it
    if hasattr(new_invoice, "total_amount"):
        new_invoice.total_amount = total_amount

    db.commit()
    db.refresh(new_invoice)
    return new_invoice

@router.get("/{invoice_id}", response_model=Invoice)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice
