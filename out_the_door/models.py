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

    profiles = relationship("Profile", uselist=False, backref="user")
    
    def as_dictionary(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }

# Profile model has a 1-to-1 relationship with Account, and a 1-to-many relationship with Photo
class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True)
    caption = Column(String(1024))
    datetime = Column(DateTime, default=datetime.datetime.now)
    age = Column(Integer)
    gender = Column(String(128))
    city = Column(String(128))
    occupation = Column(String(128))
    income = Column(Integer)
    ethnicity = Column(String(128))
    
    account_id = Column(Integer, ForeignKey('accounts.id'))
    
    photos = relationship("Photo", backref="profile")
    
    def as_dictionary(self):
        return {
            "id": self.id,
            "caption": self.caption,
            "age": self.age,
            "gender": self.gender,
            "city": self.city,
            "occupation": self.occupation,
            "income": self.income,
            "ethnicity": self.ethnicity,
            "account": self.account.as_dictionary()
        }
        
# Photo model has a many-to-1 relationship with Profile, and a 1-to-many relationship with File
class Photo(Base):
    __tablename__ = "photos"
    
    id = Column(Integer, primary_key=True)
    
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    
    files = relationship("File", backref="photo")
    
    def as_dictionary(self):
        return {
            "id": self.id,
            "profile": self.profile.as_dictionary()
        }
        
# File model has a many-to-1 relationship with Photo
class File(Base):
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    photo_id = Column(Integer, ForeignKey("photos.id"), nullable=False)
    
    def as_dictionary(self):
        return {
            "id": self.id,
            "name": self.name,
            "photo": self.photo.as_dictionary()
        }