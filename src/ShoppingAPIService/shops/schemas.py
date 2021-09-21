from pydantic import BaseModel


class Shop(BaseModel):
    name: str


class ShopResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode=True
