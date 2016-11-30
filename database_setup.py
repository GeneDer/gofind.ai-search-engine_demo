import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Posts(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    main_image_url = Column(String(2000), nullable=False)
    source_url = Column(String(2000), nullable=False)
    tags = Column(String(2000), nullable=False)
    Image_name = Column(String(200), nullable=False)

class Results(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, nullable=False)
    image_url = Column(String(2000), nullable=False)
    seller_url = Column(String(2000), nullable=False)
    seller_name = Column(String(200), nullable=False)
    item_name = Column(String(200), nullable=False)
    price = Column(String(200), nullable=False)

class Early_access(Base):
    __tablename__ = 'early_access'

    id = Column(Integer, primary_key=True)
    name = Column(String(2000), nullable=False)
    email = Column(String(2000), nullable=False)

engine = create_engine('sqlite:///search_engine_demo.db')


Base.metadata.create_all(engine)
