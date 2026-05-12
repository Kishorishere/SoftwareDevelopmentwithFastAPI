from pydantic import BaseModel
from typing import Optional


class ProductLineBase(BaseModel):
    textDescription: Optional[str] = None
    htmlDescription: Optional[str] = None


class ProductLineCreate(ProductLineBase):
    productLine: str


class ProductLineUpdate(BaseModel):
    textDescription: Optional[str] = None
    htmlDescription: Optional[str] = None


class ProductLineOut(ProductLineBase):
    productLine: str

    class Config:
        from_attributes = True
