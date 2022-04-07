from sqlalchemy import Column, Integer, String
from models import Base

class Product(Base):
    __tablename__ = 'product'
    # id = Column(Integer, primary_key=True)
    sku = Column(String(120), index=True, unique=True, primary_key=True)
    name = Column(String(120), index=True)
    description = Column(String(), index=True)
    status = Column(String(60), index=True, default='inactive')

    def __repr__(self):
        return f'<User {self.sku}>'