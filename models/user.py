from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from models.base import Base


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer , primary_key=True , nullable=False , autoincrement=True)
    name = Column(String(50) , nullable=False)
    email = Column(String , unique=True , nullable=False)
    password = Column(String , nullable=False)
    created_at = Column(DateTime , nullable=False , default=func.now())

    orders = relationship('Order' , back_populates='user' , lazy="dynamic")