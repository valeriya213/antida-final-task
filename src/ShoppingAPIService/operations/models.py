from sqlalchemy import Column
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Float, Integer, String, Date

from ..database import Base


class Operation(Base):
    __tablename__ = 'operations'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    shop_id = Column(ForeignKey('shops.id', ondelete='CASCADE'), nullable=False)
    category_id = Column(ForeignKey('categories.id', ondelete='CASCADE'))
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)

    shop = relationship('Shop', back_populates='operation')
    category = relationship('Category', back_populates='operation')
