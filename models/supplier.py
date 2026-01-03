from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.base import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)

    products = relationship(
        "Product",
        back_populates="supplier",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
