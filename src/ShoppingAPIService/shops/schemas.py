from pydantic import BaseModel


class ShopName(BaseModel):
    name: str


class Shop(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode=True
