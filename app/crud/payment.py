import logging
from sqlalchemy.orm import Session
from models import Payment
from schemas.payment import PaymentCreate, PaymentUpdate

logger = logging.getLogger(__name__)


def get_payments(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching payments skip={skip} limit={limit}")
    return db.query(Payment).offset(skip).limit(limit).all()


def get_payment(db: Session, customer_number: int, check_number: str):
    logger.info(f"Fetching payment customer={customer_number} check={check_number}")
    return db.query(Payment).filter(
        Payment.customerNumber == customer_number,
        Payment.checkNumber == check_number
    ).first()


def create_payment(db: Session, payment: PaymentCreate):
    logger.info(f"Creating payment customer={payment.customerNumber} check={payment.checkNumber}")
    obj = Payment(**payment.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_payment(db: Session, customer_number: int, check_number: str, payment: PaymentUpdate):
    logger.info(f"Updating payment customer={customer_number} check={check_number}")
    obj = db.query(Payment).filter(
        Payment.customerNumber == customer_number,
        Payment.checkNumber == check_number
    ).first()
    if not obj:
        return None
    for k, v in payment.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete_payment(db: Session, customer_number: int, check_number: str):
    logger.info(f"Deleting payment customer={customer_number} check={check_number}")
    obj = db.query(Payment).filter(
        Payment.customerNumber == customer_number,
        Payment.checkNumber == check_number
    ).first()
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj


def get_payments_by_customer(db: Session, customer_number: int):
    return db.query(Payment).filter(Payment.customerNumber == customer_number).all()
