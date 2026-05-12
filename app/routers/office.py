import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.office import OfficeOut, OfficeCreate, OfficeUpdate
import crud.office as crud

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/offices", tags=["Offices"])


@router.get("/", response_model=List[OfficeOut])
def list_offices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_offices(db, skip, limit)


@router.get("/{officeCode}", response_model=OfficeOut)
def get_office(officeCode: str, db: Session = Depends(get_db)):
    obj = crud.get_office(db, officeCode)
    if not obj:
        raise HTTPException(404, "Office not found")
    return obj


@router.post("/", response_model=OfficeOut, status_code=201)
def create_office(office: OfficeCreate, db: Session = Depends(get_db)):
    return crud.create_office(db, office)


@router.put("/{officeCode}", response_model=OfficeOut)
def update_office(officeCode: str, office: OfficeUpdate, db: Session = Depends(get_db)):
    obj = crud.update_office(db, officeCode, office)
    if not obj:
        raise HTTPException(404, "Office not found")
    return obj


@router.delete("/{officeCode}", response_model=OfficeOut)
def delete_office(officeCode: str, db: Session = Depends(get_db)):
    obj = crud.delete_office(db, officeCode)
    if not obj:
        raise HTTPException(404, "Office not found")
    return obj


@router.get("/{officeCode}/employees")
def office_employees(officeCode: str, db: Session = Depends(get_db)):
    if not crud.get_office(db, officeCode):
        raise HTTPException(404, "Office not found")
    return crud.get_office_employees(db, officeCode)
