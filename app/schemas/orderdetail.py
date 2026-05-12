from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class OrderDetailBase(BaseModel):
    quantityOrdered: int
    priceEach: Decimal
    orderLineNumber: int


class OrderDetailCreate(OrderDetailBase):
    orderNumber: int
    productCode: str


class OrderDetailUpdate(BaseModel):
    quantityOrdered: Optional[int] = None
    priceEach: Optional[Decimal] = None
    orderLineNumber: Optional[int] = None


class OrderDetailOut(OrderDetailBase):
    orderNumber: int
    productCode: str

    class Config:
        from_attributes = True
