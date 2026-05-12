import logging
from sqlalchemy.orm import Session
from sqlalchemy import text
from models import Product
from schemas.product import ProductCreate, ProductUpdate

logger = logging.getLogger(__name__)


def get_products(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching products skip={skip} limit={limit}")
    return db.query(Product).offset(skip).limit(limit).all()


def get_product(db: Session, product_code: str):
    logger.info(f"Fetching product {product_code}")
    return db.query(Product).filter(Product.productCode == product_code).first()


def create_product(db: Session, product: ProductCreate):
    logger.info(f"Creating product {product.productCode}")
    obj = Product(**product.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_product(db: Session, product_code: str, product: ProductUpdate):
    logger.info(f"Updating product {product_code}")
    obj = db.query(Product).filter(Product.productCode == product_code).first()
    if not obj:
        return None
    for k, v in product.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete_product(db: Session, product_code: str):
    logger.info(f"Deleting product {product_code}")
    obj = db.query(Product).filter(Product.productCode == product_code).first()
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj


def get_product_orderdetails(db: Session, product_code: str):
    result = db.execute(text('SELECT * FROM orderdetails WHERE "productCode" = :code'), {"code": product_code})
    return [dict(row._mapping) for row in result]
