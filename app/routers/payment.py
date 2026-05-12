import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.payment import PaymentOut, PaymentCreate, PaymentUpdate
import crud.payment as crud

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/payments", tags=["Payments"])


@router.get("/", response_model=List[PaymentOut])
def list_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_payments(db, skip, limit)


@router.get("/{customerNumber}/{checkNumber}", response_model=PaymentOut)
def get_payment(customerNumber: int, checkNumber: str, db: Session = Depends(get_db)):
    obj = crud.get_payment(db, customerNumber, checkNumber)
    if not obj:
        raise HTTPException(404, "Payment not found")
    return obj


@router.post("/", response_model=PaymentOut, status_code=201)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    return crud.create_payment(db, payment)


@router.put("/{customerNumber}/{checkNumber}", response_model=PaymentOut)
def update_payment(customerNumber: int, checkNumber: str, payment: PaymentUpdate, db: Session = Depends(get_db)):
    obj = crud.update_payment(db, customerNumber, checkNumber, payment)
    if not obj:
        raise HTTPException(404, "Payment not found")
    return obj


@router.delete("/{customerNumber}/{checkNumber}", response_model=PaymentOut)
def delete_payment(customerNumber: int, checkNumber: str, db: Session = Depends(get_db)):
    obj = crud.delete_payment(db, customerNumber, checkNumber)
    if not obj:
        raise HTTPException(404, "Payment not found")
    return obj


@router.get("/customer/{customerNumber}", response_model=List[PaymentOut])
def payments_by_customer(customerNumber: int, db: Session = Depends(get_db)):
    return crud.get_payments_by_customer(db, customerNumber)
