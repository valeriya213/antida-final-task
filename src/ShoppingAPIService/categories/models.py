from sqlalchemy import Column
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from ..database import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    account_id = Column(ForeignKey('accounts.id', ondelete='CASCADE'),
                        nullable=False)

    account = relationship('Account', back_populates='category')
    operation = relationship('Operation', cascade="all,delete", back_populates='category')
    __table_args__ = (
        UniqueConstraint('name', 'account_id',
                         name='unique_category_name_for_account'),
    )
