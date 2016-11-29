import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Main_images(Base):
    __tablename__ = 'main_images'

    id = Column(Integer, primary_key=True)
    main_image_url = Column(String(2000), nullable=False)
    source_url = Column(String(2000), nullable=False)

engine = create_engine('sqlite:///main_images.db')


Base.metadata.create_all(engine)
