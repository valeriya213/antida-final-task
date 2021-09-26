from datetime import date
from typing import Optional
from pydantic import BaseModel


class OperationRequest(BaseModel):
    type: str
    date: date
    shop_id: int
    category_id: Optional[int]
    name: str
    price: float
    amount: float


class Operation(BaseModel):
    id: int
    type: str
    date: date
    shop_id: int
    category_id: Optional[int]
    name: str
    price: float
    amount: float

    class Config:
        orm_mode = True
