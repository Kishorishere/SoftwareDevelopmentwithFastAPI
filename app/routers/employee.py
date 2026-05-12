import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.employee import EmployeeOut, EmployeeCreate, EmployeeUpdate
import crud.employee as crud

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/", response_model=List[EmployeeOut])
def list_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_employees(db, skip, limit)


@router.get("/{employeeNumber}", response_model=EmployeeOut)
def get_employee(employeeNumber: int, db: Session = Depends(get_db)):
    obj = crud.get_employee(db, employeeNumber)
    if not obj:
        raise HTTPException(404, "Employee not found")
    return obj


@router.post("/", response_model=EmployeeOut, status_code=201)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, employee)


@router.put("/{employeeNumber}", response_model=EmployeeOut)
def update_employee(employeeNumber: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    obj = crud.update_employee(db, employeeNumber, employee)
    if not obj:
        raise HTTPException(404, "Employee not found")
    return obj


@router.delete("/{employeeNumber}", response_model=EmployeeOut)
def delete_employee(employeeNumber: int, db: Session = Depends(get_db)):
    obj = crud.delete_employee(db, employeeNumber)
    if not obj:
        raise HTTPException(404, "Employee not found")
    return obj


@router.get("/{employeeNumber}/customers")
def employee_customers(employeeNumber: int, db: Session = Depends(get_db)):
    if not crud.get_employee(db, employeeNumber):
        raise HTTPException(404, "Employee not found")
    return crud.get_employee_customers(db, employeeNumber)


@router.get("/{employeeNumber}/reports")
def employee_reports(employeeNumber: int, db: Session = Depends(get_db)):
    if not crud.get_employee(db, employeeNumber):
        raise HTTPException(404, "Employee not found")
    return crud.get_employee_reports(db, employeeNumber)
