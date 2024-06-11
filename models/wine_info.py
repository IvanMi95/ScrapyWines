from sqlalchemy import Column, ForeignKey, Integer,  Float
from sqlalchemy.orm import relationship

from project.database import Base


class WineInfo(Base):
    __tablename__ = "wine_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wine_id = Column(Integer, ForeignKey('wine.id'), nullable=False)
    sale_price = Column(Float,  nullable=False)
    original_price = Column(Float,  nullable=False)
    lowest_price = Column(Float,  nullable=True)
    discount_percentage = Column(Float,  nullable=False)
    availability = Column(Integer,  nullable=True)

    wine = relationship("Wine", back_populates="wine_info")
