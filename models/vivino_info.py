from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from project.database import Base


class VivinoInfo(Base):
    __tablename__ = "vivino_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(128), unique=True, nullable=False)
    rating = Column(Float,  nullable=True)
    reviews = Column(Integer,  nullable=True)

    wine = relationship("Wine", back_populates="vivino_info")
