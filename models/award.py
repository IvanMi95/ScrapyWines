from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from project.database import Base


class Award(Base):
    __tablename__ = "award"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wine_id = Column(Integer, ForeignKey('wine.id'), nullable=False)
    critic = Column(String(128), nullable=False)
    score = Column(String(128), nullable=False)
# TODO add created at colum

    wine = relationship("Wine", back_populates="awards")
