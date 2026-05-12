import logging
from sqlalchemy.orm import Session
from models import OrderDetail
from schemas.orderdetail import OrderDetailCreate, OrderDetailUpdate

logger = logging.getLogger(__name__)


def get_orderdetails(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching orderdetails skip={skip} limit={limit}")
    return db.query(OrderDetail).offset(skip).limit(limit).all()


def get_orderdetail(db: Session, order_number: int, product_code: str):
    logger.info(f"Fetching orderdetail order={order_number} product={product_code}")
    return db.query(OrderDetail).filter(
        OrderDetail.orderNumber == order_number,
        OrderDetail.productCode == product_code
    ).first()


def create_orderdetail(db: Session, orderdetail: OrderDetailCreate):
    logger.info(f"Creating orderdetail order={orderdetail.orderNumber} product={orderdetail.productCode}")
    obj = OrderDetail(**orderdetail.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_orderdetail(db: Session, order_number: int, product_code: str, orderdetail: OrderDetailUpdate):
    logger.info(f"Updating orderdetail order={order_number} product={product_code}")
    obj = db.query(OrderDetail).filter(
        OrderDetail.orderNumber == order_number,
        OrderDetail.productCode == product_code
    ).first()
    if not obj:
        return None
    for k, v in orderdetail.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete_orderdetail(db: Session, order_number: int, product_code: str):
    logger.info(f"Deleting orderdetail order={order_number} product={product_code}")
    obj = db.query(OrderDetail).filter(
        OrderDetail.orderNumber == order_number,
        OrderDetail.productCode == product_code
    ).first()
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj


def get_orderdetails_by_order(db: Session, order_number: int):
    return db.query(OrderDetail).filter(OrderDetail.orderNumber == order_number).all()


def get_orderdetails_by_product(db: Session, product_code: str):
    return db.query(OrderDetail).filter(OrderDetail.productCode == product_code).all()
