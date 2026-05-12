from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class ProductBase(BaseModel):
    productName: str
    productLine: str
    productScale: str
    productVendor: str
    productDescription: str
    quantityInStock: int
    buyPrice: Decimal
    MSRP: Decimal


class ProductCreate(ProductBase):
    productCode: str


class ProductUpdate(BaseModel):
    productName: Optional[str] = None
    productLine: Optional[str] = None
    productScale: Optional[str] = None
    productVendor: Optional[str] = None
    productDescription: Optional[str] = None
    quantityInStock: Optional[int] = None
    buyPrice: Optional[Decimal] = None
    MSRP: Optional[Decimal] = None


class ProductOut(ProductBase):
    productCode: str

    class Config:
        from_attributes = True
