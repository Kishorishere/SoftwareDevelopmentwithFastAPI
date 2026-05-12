import logging
from sqlalchemy.orm import Session
from sqlalchemy import text
from models import Office
from schemas.office import OfficeCreate, OfficeUpdate

logger = logging.getLogger(__name__)


def get_offices(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching offices skip={skip} limit={limit}")
    return db.query(Office).offset(skip).limit(limit).all()


def get_office(db: Session, office_code: str):
    logger.info(f"Fetching office {office_code}")
    return db.query(Office).filter(Office.officeCode == office_code).first()


def create_office(db: Session, office: OfficeCreate):
    logger.info(f"Creating office {office.officeCode}")
    obj = Office(**office.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_office(db: Session, office_code: str, office: OfficeUpdate):
    logger.info(f"Updating office {office_code}")
    obj = db.query(Office).filter(Office.officeCode == office_code).first()
    if not obj:
        return None
    for k, v in office.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete_office(db: Session, office_code: str):
    logger.info(f"Deleting office {office_code}")
    obj = db.query(Office).filter(Office.officeCode == office_code).first()
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj


def get_office_employees(db: Session, office_code: str):
    result = db.execute(text('SELECT * FROM employees WHERE "officeCode" = :code'), {"code": office_code})
    return [dict(row._mapping) for row in result]
