from pydantic import BaseModel


class CategoryName(BaseModel):
    name: str


class Category(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode=True
