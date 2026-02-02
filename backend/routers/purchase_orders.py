# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from .. import models, database
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
# from email import encoders
# import smtplib, os
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
# from backend.database import get_db 
# from backend.models import PurchaseOrder, PurchaseOrderLine, POStatus 
# from backend.schemas import PurchaseOrderCreate, PurchaseOrder

# router = APIRouter(prefix="/purchase_orders", tags=["purchase_orders"])

# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587
# SMTP_USER = "yourstore@example.com"
# SMTP_PASSWORD = "yourpassword"

# def get_db():
#     db = database.SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @router.post("/auto_generate/")
# def auto_generate_pos(db: Session = Depends(get_db)):
#     products = db.query(models.Product).filter(models.Product.stock <= models.Product.reorder_level).all()
#     pos = []
#     for p in products:
#         reorder_qty = p.reorder_level * 2
#         po = models.PurchaseOrder(product_id=p.id, supplier_id=p.supplier_id, quantity=reorder_qty)
#         db.add(po)
#         db.commit()
#         db.refresh(po)
#         pos.append({
#             "po_id": po.id,
#             "product": p.name,
#             "supplier": p.supplier.name,
#             "quantity": reorder_qty,
#             "status": po.status
#         })
#     return pos

# def send_email(to_email, subject, body):
#     msg = MIMEText(body)
#     msg["Subject"] = subject
#     msg["From"] = SMTP_USER
#     msg["To"] = to_email
#     with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#         server.starttls()
#         server.login(SMTP_USER, SMTP_PASSWORD)
#         server.sendmail(SMTP_USER, [to_email], msg.as_string())

# @router.post("/{po_id}/send/")
# def send_purchase_order(po_id: int, db: Session = Depends(get_db)):
#     po = db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == po_id).first()
#     if not po:
#         raise HTTPException(status_code=404, detail="PO not found")
#     supplier = po.supplier
#     product = po.product
#     body = f"""
#     Dear {supplier.name},

#     Please find below the purchase order details:

#     Product: {product.name}
#     Quantity: {po.quantity}
#     Unit Price: {product.price}
#     Total: {product.price * po.quantity}

#     Kindly confirm delivery timeline.

#     Regards,
#     Pet Supply Store
#     """
#     send_email(supplier.contact_email, f"Purchase Order #{po.id}", body)
#     po.status = "Sent"
#     db.commit()
#     return {"message": f"PO #{po.id} sent to {supplier.contact_email}"}

# def generate_po_pdf(po, supplier):
#     filename = f"PO_{po.id}.pdf"
#     filepath = os.path.join("purchase_orders", filename)
#     os.makedirs("purchase_orders", exist_ok=True)
#     c = canvas.Canvas(filepath, pagesize=A4)
#     c.setFont("Helvetica", 12)
#     c.drawString(100, 800, f"Purchase Order #{po.id}")
#     c.drawString(100, 780, f"Supplier: {supplier.name}")
#     c.drawString(100, 760, f"Email: {supplier.contact_email}")
#     c.drawString(100, 740, f"Phone: {supplier.phone}")
#     y = 700
#     total = 0
#     for line in po.lines:
#         product = line.product
#         subtotal = line.unit_price * line.quantity
#         total += subtotal
#         c.drawString(100, y, f"{product.name} - Qty: {line.quantity} @ {line.unit_price} = {subtotal}")
#         y -= 20
#     c.drawString(100, y-20, f"Total: {total}")
#     c.save()
#     return filepath

# def send_email_with_pdf(to_email, subject, body, pdf_path):
#     msg = MIMEMultipart()
#     msg["Subject"] = subject
#     msg["From"] = SMTP_USER
#     msg["To"] = to_email
#     msg.attach(MIMEText(body, "plain"))
#     with open(pdf_path, "rb") as f:
#         part = MIMEBase("application", "octet-stream")
#         part.set_payload(f.read())
#         encoders.encode_base64(part)
#         part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(pdf_path)}")
#         msg.attach(part)
#     with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#         server.starttls()
#         server.login(SMTP_USER, SMTP_PASSWORD)
#         server.sendmail(SMTP_USER, [to_email], msg.as_string())

# @router.post("/{po_id}/send_pdf/")
# def send_po_with_pdf(po_id: int, db: Session = Depends(get_db)):
#     po = db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == po_id).first()
#     if not po:
#         raise HTTPException(status_code=404, detail="PO not found")
#     supplier = po.supplier
#     pdf_path = generate_po_pdf(po, supplier)
#     body = f"Dear {supplier.name},\n\nPlease find attached Purchase Order #{po.id}.\n\nRegards,\nPet Supply Store"
#     send_email_with_pdf(supplier.contact_email, f"Purchase Order #{po.id}", body, pdf_path)
#     po.status = "Sent"
#     db.commit()
#     return {"message": f"PO #{po.id} sent to {supplier.contact_email} with PDF attachment"}

# @router.post("/{po_id}/update_status/")
# def update_po_status(po_id: int, new_status: str, db: Session = Depends(get_db)):
#     valid_statuses = ["Draft", "Sent", "Confirmed", "Delivered", "Closed"]
#     if new_status not in valid_statuses:
#         raise HTTPException(status_code=400, detail="Invalid status")
#     po = db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == po_id).first()
#     if not po:
#         raise HTTPException(status_code=404, detail="PO not found")
#     po.status = new_status
#     db.commit()
#     return {"po_id": po.id, "new_status": po.status}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import PurchaseOrder, PurchaseOrderLine, POStatus, Product, Supplier
from backend.schemas import PurchaseOrderCreate, PurchaseOrder

router = APIRouter(prefix="/purchase_orders", tags=["purchase_orders"])

@router.post("/", response_model=PurchaseOrder)
def create_po(po: PurchaseOrderCreate, db: Session = Depends(get_db)):
    new_po = PurchaseOrder(supplier_id=po.supplier_id, status=po.status)
    db.add(new_po)
    db.flush()  # get PO id before adding lines

    for line in po.lines:
        db.add(PurchaseOrderLine(
            purchase_order_id=new_po.id,
            product_id=line.product_id,
            quantity=line.quantity,
            unit_price=line.unit_price
        ))

    db.commit()
    db.refresh(new_po)
    return new_po

@router.get("/{po_id}", response_model=PurchaseOrder)
def get_po(po_id: int, db: Session = Depends(get_db)):
    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if not po:
        raise HTTPException(status_code=404, detail="PO not found")
    return po

@router.put("/{po_id}/status", response_model=PurchaseOrder)
def update_po_status(po_id: int, status: POStatus, db: Session = Depends(get_db)):
    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if not po:
        raise HTTPException(status_code=404, detail="PO not found")
    po.status = status
    db.commit()
    db.refresh(po)
    return po

