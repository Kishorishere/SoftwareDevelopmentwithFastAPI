import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.order import OrderOut, OrderCreate, OrderUpdate
import crud.order as crud

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=List[OrderOut])
def list_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orders(db, skip, limit)


@router.get("/{orderNumber}", response_model=OrderOut)
def get_order(orderNumber: int, db: Session = Depends(get_db)):
    obj = crud.get_order(db, orderNumber)
    if not obj:
        raise HTTPException(404, "Order not found")
    return obj


@router.post("/", response_model=OrderOut, status_code=201)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)


@router.put("/{orderNumber}", response_model=OrderOut)
def update_order(orderNumber: int, order: OrderUpdate, db: Session = Depends(get_db)):
    obj = crud.update_order(db, orderNumber, order)
    if not obj:
        raise HTTPException(404, "Order not found")
    return obj


@router.delete("/{orderNumber}", response_model=OrderOut)
def delete_order(orderNumber: int, db: Session = Depends(get_db)):
    obj = crud.delete_order(db, orderNumber)
    if not obj:
        raise HTTPException(404, "Order not found")
    return obj


@router.get("/{orderNumber}/orderdetails")
def order_details(orderNumber: int, db: Session = Depends(get_db)):
    if not crud.get_order(db, orderNumber):
        raise HTTPException(404, "Order not found")
    return crud.get_order_details(db, orderNumber)


@router.get("/customer/{customerNumber}", response_model=List[OrderOut])
def orders_by_customer(customerNumber: int, db: Session = Depends(get_db)):
    return crud.get_orders_by_customer(db, customerNumber)
