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
    image_name = Column(String(200), nullable=False)

class Segmented(Base):
    __tablename__ = 'segmented'

    id = Column(Integer, primary_key=True)
    segmented_image_url = Column(String(2000), nullable=False)
    post_id = Column(Integer, nullable=False)

class Results(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    segmented_id = Column(Integer, nullable=False)
    image_url = Column(String(2000), nullable=False)
    seller_url = Column(String(2000), nullable=False)
    seller_name = Column(String(200), nullable=False)
    item_name = Column(String(200), nullable=False)
    price = Column(String(200), nullable=False)

class Stay_updated(Base):
    __tablename__ = 'stay_updated'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)

class Influencer(Base):
    __tablename__ = 'influencer'

    id = Column(Integer, primary_key=True)
    tumblr_id = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)

class Advertiser(Base):
    __tablename__ = 'advertiser'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    company = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    phone = Column(String(20), nullable=False)
    message = Column(String(2000), nullable=False)

class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    message = Column(String(2000), nullable=False)

engine = create_engine('sqlite:///search_engine_demo.db')


Base.metadata.create_all(engine)
