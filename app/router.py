import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import CustomerOut, CustomerCreate, CustomerUpdate
import crud

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/", response_model=List[CustomerOut])
def list_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"GET /customers skip={skip} limit={limit}")
    return crud.get_customers(db, skip=skip, limit=limit)


@router.get("/{customerNumber}", response_model=CustomerOut)
def get_customer(customerNumber: int, db: Session = Depends(get_db)):
    logger.info(f"GET /customers/{customerNumber}")
    customer = crud.get_customer(db, customerNumber)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.post("/", response_model=CustomerOut, status_code=201)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    logger.info(f"POST /customers")
    return crud.create_customer(db, customer)


@router.put("/{customerNumber}", response_model=CustomerOut)
def update_customer(customerNumber: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    logger.info(f"PUT /customers/{customerNumber}")
    updated = crud.update_customer(db, customerNumber, customer)
    if not updated:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated


@router.delete("/{customerNumber}", response_model=CustomerOut)
def delete_customer(customerNumber: int, db: Session = Depends(get_db)):
    logger.info(f"DELETE /customers/{customerNumber}")
    deleted = crud.delete_customer(db, customerNumber)
    if not deleted:
        raise HTTPException(status_code=404, detail="Customer not found")
    return deleted


@router.get("/{customerNumber}/orders")
def get_customer_orders(customerNumber: int, db: Session = Depends(get_db)):
    logger.info(f"GET /customers/{customerNumber}/orders")
    customer = crud.get_customer(db, customerNumber)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return crud.get_customer_orders(db, customerNumber)


@router.get("/{customerNumber}/payments")
def get_customer_payments(customerNumber: int, db: Session = Depends(get_db)):
    logger.info(f"GET /customers/{customerNumber}/payments")
    customer = crud.get_customer(db, customerNumber)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return crud.get_customer_payments(db, customerNumber)
