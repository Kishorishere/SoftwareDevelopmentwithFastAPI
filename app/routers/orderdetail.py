import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.orderdetail import OrderDetailOut, OrderDetailCreate, OrderDetailUpdate
import crud.orderdetail as crud

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/orderdetails", tags=["OrderDetails"])


@router.get("/", response_model=List[OrderDetailOut])
def list_orderdetails(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orderdetails(db, skip, limit)


@router.get("/{orderNumber}/{productCode}", response_model=OrderDetailOut)
def get_orderdetail(orderNumber: int, productCode: str, db: Session = Depends(get_db)):
    obj = crud.get_orderdetail(db, orderNumber, productCode)
    if not obj:
        raise HTTPException(404, "OrderDetail not found")
    return obj


@router.post("/", response_model=OrderDetailOut, status_code=201)
def create_orderdetail(orderdetail: OrderDetailCreate, db: Session = Depends(get_db)):
    return crud.create_orderdetail(db, orderdetail)


@router.put("/{orderNumber}/{productCode}", response_model=OrderDetailOut)
def update_orderdetail(orderNumber: int, productCode: str, orderdetail: OrderDetailUpdate, db: Session = Depends(get_db)):
    obj = crud.update_orderdetail(db, orderNumber, productCode, orderdetail)
    if not obj:
        raise HTTPException(404, "OrderDetail not found")
    return obj


@router.delete("/{orderNumber}/{productCode}", response_model=OrderDetailOut)
def delete_orderdetail(orderNumber: int, productCode: str, db: Session = Depends(get_db)):
    obj = crud.delete_orderdetail(db, orderNumber, productCode)
    if not obj:
        raise HTTPException(404, "OrderDetail not found")
    return obj


@router.get("/order/{orderNumber}", response_model=List[OrderDetailOut])
def orderdetails_by_order(orderNumber: int, db: Session = Depends(get_db)):
    return crud.get_orderdetails_by_order(db, orderNumber)


@router.get("/product/{productCode}", response_model=List[OrderDetailOut])
def orderdetails_by_product(productCode: str, db: Session = Depends(get_db)):
    return crud.get_orderdetails_by_product(db, productCode)
