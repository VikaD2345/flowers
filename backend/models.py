from sqlalchemy import Column, Integer, String, Numeric
from database import Base

class FlowerModel(Base):
    __tablename__ = "flowers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    image_url = Column(String, nullable=False)
