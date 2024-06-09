from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from project.database import Base


class Wine(Base):
    __tablename__ = "wine"

    id = Column(Integer, primary_key=True, autoincrement=True)
    website = Column(String(128),  nullable=False)
    url = Column(String(128), unique=True, nullable=False)
    name = Column(String(128), nullable=False)
    sale_price = Column(Float,  nullable=False)
    original_price = Column(Float,  nullable=False)
    lowest_price = Column(Float,  nullable=True)
    discount_percentage = Column(Float,  nullable=False)
    availability = Column(Integer,  nullable=True)
    grape_variety = Column(String(128),  nullable=True)
    appellation = Column(String(128),  nullable=True)
    alcohol_content = Column(Float,  nullable=True)
    serving_temperature = Column(String(128),  nullable=True)
    wine_type = Column(String(128), nullable=False)
    vivino_rating = Column(Float,  nullable=True)
    vivino_reviews = Column(Integer,  nullable=True)
    vivino_url = Column(String(128), unique=True, nullable=False)

    awards = relationship("Award", back_populates="wine")


class Award(Base):
    __tablename__ = "award"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wine_id = Column(Integer, ForeignKey('wine.id'), nullable=False)
    critic = Column(String(128), nullable=False)
    score = Column(String(128), nullable=False)

    wine = relationship("Wine", back_populates="awards")
