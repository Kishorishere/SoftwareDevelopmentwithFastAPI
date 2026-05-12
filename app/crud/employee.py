import logging
from sqlalchemy.orm import Session
from sqlalchemy import text
from models import Employee
from schemas.employee import EmployeeCreate, EmployeeUpdate

logger = logging.getLogger(__name__)


def get_employees(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching employees skip={skip} limit={limit}")
    return db.query(Employee).offset(skip).limit(limit).all()


def get_employee(db: Session, employee_number: int):
    logger.info(f"Fetching employee {employee_number}")
    return db.query(Employee).filter(Employee.employeeNumber == employee_number).first()


def create_employee(db: Session, employee: EmployeeCreate):
    logger.info(f"Creating employee {employee.employeeNumber}")
    obj = Employee(**employee.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_employee(db: Session, employee_number: int, employee: EmployeeUpdate):
    logger.info(f"Updating employee {employee_number}")
    obj = db.query(Employee).filter(Employee.employeeNumber == employee_number).first()
    if not obj:
        return None
    for k, v in employee.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete_employee(db: Session, employee_number: int):
    logger.info(f"Deleting employee {employee_number}")
    obj = db.query(Employee).filter(Employee.employeeNumber == employee_number).first()
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj


def get_employee_customers(db: Session, employee_number: int):
    result = db.execute(
        text('SELECT * FROM customers WHERE "salesRepEmployeeNumber" = :num'),
        {"num": employee_number}
    )
    return [dict(row._mapping) for row in result]


def get_employee_reports(db: Session, employee_number: int):
    result = db.execute(
        text('SELECT * FROM employees WHERE "reportsTo" = :num'),
        {"num": employee_number}
    )
    return [dict(row._mapping) for row in result]
