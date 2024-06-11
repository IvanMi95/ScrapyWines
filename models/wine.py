from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from project.database import Base


class Wine(Base):
    __tablename__ = "wine"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vivino_id = Column(Integer, ForeignKey('vivino_info.id'), nullable=False)
    website = Column(String(128),  nullable=False)
    url = Column(String(128), unique=True, nullable=False)
    name = Column(String(128), nullable=False)
    grape_variety = Column(String(128),  nullable=True)
    appellation = Column(String(128),  nullable=True)
    alcohol_content = Column(Float,  nullable=True)
    serving_temperature = Column(String(128),  nullable=True)
    wine_type = Column(String(128), nullable=False)

    awards = relationship("Award", back_populates="wine")
    wine_info = relationship("WineInfo", back_populates="wine")
    vivino_info = relationship("VivinoInfo", back_populates="wine")
# TODO maybe change info relative to webisite to wine info
