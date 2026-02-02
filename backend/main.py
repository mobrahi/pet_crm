from fastapi import FastAPI
from . import models, database
from .routers import customers, products, suppliers, invoices, purchase_orders, reports
import smtplib 
from email.mime.text import MIMEText 
from fastapi import HTTPException, FastAPI, Depends
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from email.mime.multipart import MIMEMultipart 
from email.mime.base import MIMEBase 
from email import encoders
from sqlalchemy.orm import Session
from backend.routers import all_routers
from backend.database import Base, engine 
from backend import models # triggers auto-discovery

SMTP_SERVER = "smtp.gmail.com" 
SMTP_PORT = 587 
SMTP_USER = "yourstore@example.com" 
SMTP_PASSWORD = "yourpassword"

#models.Base.metadata.create_all(bind=database.engine)
# Create tables automatically 
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pet Supply Store CRM")

# Register all routers automatically 
for router in all_routers: 
    app.include_router(router)

@app.get("/")
def root():
    return {"message": "Pet CRM API is running!"}