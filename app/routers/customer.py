import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.customer import CustomerOut, CustomerCreate, CustomerUpdate
import crud.customer as crud

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/", response_model=List[CustomerOut])
def list_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"GET /customers")
    return crud.get_customers(db, skip, limit)


@router.get("/{customerNumber}", response_model=CustomerOut)
def get_customer(customerNumber: int, db: Session = Depends(get_db)):
    logger.info(f"GET /customers/{customerNumber}")
    obj = crud.get_customer(db, customerNumber)
    if not obj:
        raise HTTPException(404, "Customer not found")
    return obj


@router.post("/", response_model=CustomerOut, status_code=201)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)


@router.put("/{customerNumber}", response_model=CustomerOut)
def update_customer(customerNumber: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    obj = crud.update_customer(db, customerNumber, customer)
    if not obj:
        raise HTTPException(404, "Customer not found")
    return obj


@router.delete("/{customerNumber}", response_model=CustomerOut)
def delete_customer(customerNumber: int, db: Session = Depends(get_db)):
    obj = crud.delete_customer(db, customerNumber)
    if not obj:
        raise HTTPException(404, "Customer not found")
    return obj


@router.get("/{customerNumber}/orders")
def customer_orders(customerNumber: int, db: Session = Depends(get_db)):
    if not crud.get_customer(db, customerNumber):
        raise HTTPException(404, "Customer not found")
    return crud.get_customer_orders(db, customerNumber)


@router.get("/{customerNumber}/payments")
def customer_payments(customerNumber: int, db: Session = Depends(get_db)):
    if not crud.get_customer(db, customerNumber):
        raise HTTPException(404, "Customer not found")
    return crud.get_customer_payments(db, customerNumber)
