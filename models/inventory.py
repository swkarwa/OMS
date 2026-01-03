from sqlalchemy import Column, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base


class Inventory(Base):

    __tablename__ = 'inventory'

    id = Column(Integer , primary_key=True , nullable=False , autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), unique=True, nullable=False)
    quantity = Column(Integer , nullable=False)
    updated_at = Column(DateTime(timezone=True) , nullable=False , onupdate=func.now() , server_default=func.now())

    product = relationship('Product' , back_populates='inventory')
