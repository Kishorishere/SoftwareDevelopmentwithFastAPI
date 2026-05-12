from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import date


class PaymentBase(BaseModel):
    paymentDate: date
    amount: Decimal


class PaymentCreate(PaymentBase):
    customerNumber: int
    checkNumber: str


class PaymentUpdate(BaseModel):
    paymentDate: Optional[date] = None
    amount: Optional[Decimal] = None


class PaymentOut(PaymentBase):
    customerNumber: int
    checkNumber: str

    class Config:
        from_attributes = True
