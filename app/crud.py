import logging
from sqlalchemy.orm import Session
from models import Customer
from schemas import CustomerCreate, CustomerUpdate

logger = logging.getLogger(__name__)


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching customers with skip={skip}, limit={limit}")
    return db.query(Customer).offset(skip).limit(limit).all()


def get_customer(db: Session, customer_id: int):
    logger.info(f"Fetching customer with id={customer_id}")
    return db.query(Customer).filter(Customer.customerNumber == customer_id).first()


def create_customer(db: Session, customer: CustomerCreate):
    logger.info(f"Creating customer: {customer.customerNumber}")
    db_customer = Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def update_customer(db: Session, customer_id: int, customer: CustomerUpdate):
    logger.info(f"Updating customer: {customer_id}")
    db_customer = db.query(Customer).filter(Customer.customerNumber == customer_id).first()
    if not db_customer:
        return None
    for key, value in customer.model_dump(exclude_unset=True).items():
        setattr(db_customer, key, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def delete_customer(db: Session, customer_id: int):
    logger.info(f"Deleting customer: {customer_id}")
    db_customer = db.query(Customer).filter(Customer.customerNumber == customer_id).first()
    if not db_customer:
        return None
    db.delete(db_customer)
    db.commit()
    return db_customer


def get_customer_orders(db: Session, customer_id: int):
    from sqlalchemy import text
    logger.info(f"Fetching orders for customer: {customer_id}")
    result = db.execute(
        text('SELECT * FROM orders WHERE "customerNumber" = :id'),
        {"id": customer_id}
    )
    return [dict(row._mapping) for row in result]


def get_customer_payments(db: Session, customer_id: int):
    from sqlalchemy import text
    logger.info(f"Fetching payments for customer: {customer_id}")
    result = db.execute(
        text('SELECT * FROM payments WHERE "customerNumber" = :id'),
        {"id": customer_id}
    )
    return [dict(row._mapping) for row in result]
