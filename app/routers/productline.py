import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.productline import ProductLineOut, ProductLineCreate, ProductLineUpdate
import crud.productline as crud

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/productlines", tags=["ProductLines"])


@router.get("/", response_model=List[ProductLineOut])
def list_productlines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_productlines(db, skip, limit)


@router.get("/{productLine}", response_model=ProductLineOut)
def get_productline(productLine: str, db: Session = Depends(get_db)):
    obj = crud.get_productline(db, productLine)
    if not obj:
        raise HTTPException(404, "ProductLine not found")
    return obj


@router.post("/", response_model=ProductLineOut, status_code=201)
def create_productline(productline: ProductLineCreate, db: Session = Depends(get_db)):
    return crud.create_productline(db, productline)


@router.put("/{productLine}", response_model=ProductLineOut)
def update_productline(productLine: str, productline: ProductLineUpdate, db: Session = Depends(get_db)):
    obj = crud.update_productline(db, productLine, productline)
    if not obj:
        raise HTTPException(404, "ProductLine not found")
    return obj


@router.delete("/{productLine}", response_model=ProductLineOut)
def delete_productline(productLine: str, db: Session = Depends(get_db)):
    obj = crud.delete_productline(db, productLine)
    if not obj:
        raise HTTPException(404, "ProductLine not found")
    return obj


@router.get("/{productLine}/products")
def productline_products(productLine: str, db: Session = Depends(get_db)):
    if not crud.get_productline(db, productLine):
        raise HTTPException(404, "ProductLine not found")
    return crud.get_productline_products(db, productLine)
