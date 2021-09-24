from sqlalchemy import Column
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from ..database import Base


class Shop(Base):
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    account_id = Column(ForeignKey('accounts.id', ondelete='CASCADE'),
                        nullable=False)

    account = relationship('Account', back_populates='shop')
    operation = relationship('Operation', back_populates='shop')
    __table_args__ = (
        UniqueConstraint('name', 'account_id',
                         name='unique_shop_name_for_account'),
    )
