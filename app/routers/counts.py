import logging
import asyncio
import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Counts"])

TABLES = ["customers", "orders", "products", "employees", "offices", "payments", "orderdetails", "productlines"]


def _count_table(db: Session, table: str) -> int:
    try:
        result = db.execute(text(f'SELECT COUNT(*) FROM "{table}"'))
        count = result.scalar()
        logger.info(f"Count {table}: {count}")
        return count or 0
    except Exception as e:
        logger.error(f"Error counting {table}: {e}")
        return 0


@router.get("/customers/count")
def count_customers(db: Session = Depends(get_db)):
    return {"customers": _count_table(db, "customers")}

@router.get("/orders/count")
def count_orders(db: Session = Depends(get_db)):
    return {"orders": _count_table(db, "orders")}

@router.get("/products/count")
def count_products(db: Session = Depends(get_db)):
    return {"products": _count_table(db, "products")}

@router.get("/employees/count")
def count_employees(db: Session = Depends(get_db)):
    return {"employees": _count_table(db, "employees")}

@router.get("/offices/count")
def count_offices(db: Session = Depends(get_db)):
    return {"offices": _count_table(db, "offices")}

@router.get("/payments/count")
def count_payments(db: Session = Depends(get_db)):
    return {"payments": _count_table(db, "payments")}

@router.get("/orderdetails/count")
def count_orderdetails(db: Session = Depends(get_db)):
    return {"orderdetails": _count_table(db, "orderdetails")}

@router.get("/productlines/count")
def count_productlines(db: Session = Depends(get_db)):
    return {"productlines": _count_table(db, "productlines")}


@router.get("/overall_counts")
async def overall_counts(db: Session = Depends(get_db)):
    logger.info("GET /overall_counts - starting concurrent gather")
    start = time.time()
    loop = asyncio.get_event_loop()

    async def async_count(table: str):
        return await loop.run_in_executor(None, _count_table, db, table)

    results = await asyncio.gather(*[async_count(t) for t in TABLES])
    elapsed = time.time() - start
    logger.info(f"overall_counts completed in {elapsed:.3f}s")
    return dict(zip(TABLES, results))
