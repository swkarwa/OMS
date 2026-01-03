from sqlalchemy import Column, Integer, String, Float, func, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    name = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())

    supplier = relationship(
        "Supplier",
        back_populates="products",
        lazy="selectin",
    )

    inventory = relationship("Inventory", uselist=False, back_populates="product", lazy="selectin")

    order_items = relationship("OrderItem", back_populates="product")

    categories = relationship(
        "Category",
        back_populates="products",
        secondary="product_category",
        lazy="selectin",
    )
