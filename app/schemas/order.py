from pydantic import BaseModel
from typing import Optional, Literal
from datetime import date


OrderStatus = Literal["Shipped", "Resolved", "Cancelled", "On Hold", "Disputed", "In Process"]


class OrderBase(BaseModel):
    orderDate: date
    requiredDate: date
    shippedDate: Optional[date] = None
    status: OrderStatus
    comments: Optional[str] = None
    customerNumber: int


class OrderCreate(OrderBase):
    orderNumber: int


class OrderUpdate(BaseModel):
    orderDate: Optional[date] = None
    requiredDate: Optional[date] = None
    shippedDate: Optional[date] = None
    status: Optional[OrderStatus] = None
    comments: Optional[str] = None
    customerNumber: Optional[int] = None


class OrderOut(OrderBase):
    orderNumber: int

    class Config:
        from_attributes = True
