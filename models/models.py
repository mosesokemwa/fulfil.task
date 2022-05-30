from sqlalchemy import Column, Integer, String
from models import Base


class Product(Base):
    __tablename__ = "product"
    sku = Column(String(120), index=True, unique=True, primary_key=True)
    name = Column(String(120), index=True)
    description = Column(String(), index=True)
    status = Column(String(60), index=True, default="inactive")

    def __repr__(self):
        return f"<Product {self.sku}>"


class Data(Base):
    __tablename__ = "data"
    sku = Column(String(120), primary_key=True)
    task_id = Column(String(120), index=True)

    def __repr__(self):
        return f"<Data {self.sku}>"