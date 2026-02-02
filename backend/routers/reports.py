from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database

router = APIRouter(prefix="/reports", tags=["reports"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/low_stock/")
def low_stock_report(db: Session = Depends(get_db)):
    products = db.query(models.Product).filter(models.Product.stock <= models.Product.reorder_level).all()
    return [{"product": p.name, "stock": p.stock, "reorder_level": p.reorder_level} for p in products]

@router.get("/reorder_requests/")
def reorder_requests(db: Session = Depends(get_db)):
    products = db.query(models.Product).filter(models.Product.stock <= models.Product.reorder_level).all()
    return [{
        "product": p.name,
        "stock": p.stock,
        "supplier": p.supplier.name,
        "contact_email": p.supplier.contact_email
    } for p in products]

@router.get("/supplier_performance/")
def supplier_performance(db: Session = Depends(get_db)):
    suppliers = db.query(models.Supplier).all()
    report = []
    for s in suppliers:
        pos = db.query(models.PurchaseOrder).filter(models.PurchaseOrder.supplier_id == s.id).all()
        if not pos:
            continue
        confirm_times = [(po.confirmed_at - po.sent_at).days for po in pos if po.confirmed_at and po.sent_at]
        delivery_times = [(po.delivered_at - po.confirmed_at).days for po in pos if po.delivered_at and po.confirmed_at]
        on_time = [1 for po in pos if po.delivered_at and po.expected_delivery and po.delivered_at <= po.expected_delivery]
        avg_confirm = sum(confirm_times)/len(confirm_times) if confirm_times else None
        avg_delivery = sum(delivery_times)/len(delivery_times) if delivery_times else None
        on_time_rate = len(on_time)/len(pos) if pos else 0
        reliability_score = ((1/(avg_confirm+1) + 1/(avg_delivery+1) + on_time_rate) / 3) if avg_confirm and avg_delivery else None
        report.append({
            "supplier": s.name,
            "avg_confirmation_days": avg_confirm,
            "avg_delivery_days": avg_delivery,
            "on_time_rate": round(on_time_rate*100, 2),
            "reliability_score": reliability_score
        })
    return report
