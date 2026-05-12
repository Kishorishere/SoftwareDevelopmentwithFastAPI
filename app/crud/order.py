import logging
from sqlalchemy.orm import Session
from sqlalchemy import text
from models import Order
from schemas.order import OrderCreate, OrderUpdate

logger = logging.getLogger(__name__)


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching orders skip={skip} limit={limit}")
    return db.query(Order).offset(skip).limit(limit).all()


def get_order(db: Session, order_number: int):
    logger.info(f"Fetching order {order_number}")
    return db.query(Order).filter(Order.orderNumber == order_number).first()


def create_order(db: Session, order: OrderCreate):
    logger.info(f"Creating order {order.orderNumber}")
    obj = Order(**order.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_order(db: Session, order_number: int, order: OrderUpdate):
    logger.info(f"Updating order {order_number}")
    obj = db.query(Order).filter(Order.orderNumber == order_number).first()
    if not obj:
        return None
    for k, v in order.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete_order(db: Session, order_number: int):
    logger.info(f"Deleting order {order_number}")
    obj = db.query(Order).filter(Order.orderNumber == order_number).first()
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj


def get_order_details(db: Session, order_number: int):
    result = db.execute(text('SELECT * FROM orderdetails WHERE "orderNumber" = :num'), {"num": order_number})
    return [dict(row._mapping) for row in result]


def get_orders_by_customer(db: Session, customer_number: int):
    return db.query(Order).filter(Order.customerNumber == customer_number).all()
