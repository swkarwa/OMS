from sqlalchemy import Integer, Column, Float, Boolean, String, func, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer , primary_key=True , nullable=False , autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total_amount = Column(Float , nullable=False)
    status = Column(String , nullable=False)
    created_at = Column(DateTime , nullable=False , default=func.now())

    user = relationship('User' , back_populates='orders')
    order_items = relationship(
        'OrderItem',
        back_populates='order'
    )
