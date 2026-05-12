import logging
from sqlalchemy.orm import Session
from sqlalchemy import text
from models import Customer
from schemas.customer import CustomerCreate, CustomerUpdate

logger = logging.getLogger(__name__)


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching customers skip={skip} limit={limit}")
    return db.query(Customer).offset(skip).limit(limit).all()


def get_customer(db: Session, customer_id: int):
    logger.info(f"Fetching customer id={customer_id}")
    return db.query(Customer).filter(Customer.customerNumber == customer_id).first()


def create_customer(db: Session, customer: CustomerCreate):
    logger.info(f"Creating customer {customer.customerNumber}")
    obj = Customer(**customer.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_customer(db: Session, customer_id: int, customer: CustomerUpdate):
    logger.info(f"Updating customer {customer_id}")
    obj = db.query(Customer).filter(Customer.customerNumber == customer_id).first()
    if not obj:
        return None
    for k, v in customer.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete_customer(db: Session, customer_id: int):
    logger.info(f"Deleting customer {customer_id}")
    obj = db.query(Customer).filter(Customer.customerNumber == customer_id).first()
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj


def get_customer_orders(db: Session, customer_id: int):
    result = db.execute(text('SELECT * FROM orders WHERE "customerNumber" = :id'), {"id": customer_id})
    return [dict(row._mapping) for row in result]


def get_customer_payments(db: Session, customer_id: int):
    result = db.execute(text('SELECT * FROM payments WHERE "customerNumber" = :id'), {"id": customer_id})
    return [dict(row._mapping) for row in result]
