import os.path
import datetime

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship

from out_the_door import app
from .database import Base, engine

class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(128), nullable=False, unique=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    
    profiles = relationship("Profile", backref="user")

class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, default=datetime.datetime.now)
    caption = Column(Text(1024))
    age = Column(Integer)
    gender = Column(String(128))
    city = Column(String(128))
    occupation = Column(String(128))
    income = Column(Integer)
    ethnicity = Column(String(128))
    
    account_id = Column(Integer, ForeignKey('accounts.id'))