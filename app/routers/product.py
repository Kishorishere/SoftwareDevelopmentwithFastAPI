import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.product import ProductOut, ProductCreate, ProductUpdate
import crud.product as crud

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[ProductOut])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_products(db, skip, limit)


@router.get("/{productCode}", response_model=ProductOut)
def get_product(productCode: str, db: Session = Depends(get_db)):
    obj = crud.get_product(db, productCode)
    if not obj:
        raise HTTPException(404, "Product not found")
    return obj


@router.post("/", response_model=ProductOut, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)


@router.put("/{productCode}", response_model=ProductOut)
def update_product(productCode: str, product: ProductUpdate, db: Session = Depends(get_db)):
    obj = crud.update_product(db, productCode, product)
    if not obj:
        raise HTTPException(404, "Product not found")
    return obj


@router.delete("/{productCode}", response_model=ProductOut)
def delete_product(productCode: str, db: Session = Depends(get_db)):
    obj = crud.delete_product(db, productCode)
    if not obj:
        raise HTTPException(404, "Product not found")
    return obj


@router.get("/{productCode}/orderdetails")
def product_orderdetails(productCode: str, db: Session = Depends(get_db)):
    if not crud.get_product(db, productCode):
        raise HTTPException(404, "Product not found")
    return crud.get_product_orderdetails(db, productCode)
