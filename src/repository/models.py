# models.py
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class RoleEnum(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

class PrivateEnum(str, enum.Enum):
    PRIVATE = "private"
    PUBLIC = "public"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER, index= True)
    catalogs = relationship("Catalog", back_populates="user")

class Catalog(Base):
    __tablename__ = "catalogs"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    date = Column(DateTime(timezone=True), server_default=func.now())
    private = Column(Enum(PrivateEnum), default=PrivateEnum.PRIVATE)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="catalogs")
    articles = relationship("Article", back_populates="catalog")

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(String)
    category = Column(String(100))
    publication = Column(DateTime(timezone=True), server_default=func.now())
    catalog_id = Column(Integer, ForeignKey("catalogs.id"))
    catalog = relationship("Catalog", back_populates="articles")