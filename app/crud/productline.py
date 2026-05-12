import logging
from sqlalchemy.orm import Session
from sqlalchemy import text
from models import ProductLine
from schemas.productline import ProductLineCreate, ProductLineUpdate

logger = logging.getLogger(__name__)


def get_productlines(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching productlines skip={skip} limit={limit}")
    return db.query(ProductLine).offset(skip).limit(limit).all()


def get_productline(db: Session, product_line: str):
    logger.info(f"Fetching productline {product_line}")
    return db.query(ProductLine).filter(ProductLine.productLine == product_line).first()


def create_productline(db: Session, productline: ProductLineCreate):
    logger.info(f"Creating productline {productline.productLine}")
    obj = ProductLine(**productline.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_productline(db: Session, product_line: str, productline: ProductLineUpdate):
    logger.info(f"Updating productline {product_line}")
    obj = db.query(ProductLine).filter(ProductLine.productLine == product_line).first()
    if not obj:
        return None
    for k, v in productline.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete_productline(db: Session, product_line: str):
    logger.info(f"Deleting productline {product_line}")
    obj = db.query(ProductLine).filter(ProductLine.productLine == product_line).first()
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj


def get_productline_products(db: Session, product_line: str):
    result = db.execute(text('SELECT * FROM products WHERE "productLine" = :pl'), {"pl": product_line})
    return [dict(row._mapping) for row in result]
