from sqlalchemy import Column, Integer, ForeignKey

from models.base import Base


class Product_Category(Base):

    __tablename__ = 'product_category'

    id = Column(Integer , primary_key=True , nullable=False , autoincrement=True)
    product_id = Column(Integer , ForeignKey('products.id') , nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)