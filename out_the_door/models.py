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
    
    # add the path property here ?
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
            "account": {
                "id": self.account.id,
                "username": self.account.username,
                "name": self.account.name,
                "email": self.account.email,
                "password": self.account.password
            }
        }
        
# Photo model has a many-to-1 relationship with Profile, and a 1-to-many relationship with File
class Photo(Base):
    __tablename__ = "photos"
    
    id = Column(Integer, primary_key=True)
    
    profile_id = Column(Integer, ForeignKey("profile.id"), nullable=False)
    
    files = relationship("File", backref="photo")
    
    # add the path property here?
    def as_dictionary(self):
        return {
            "id": self.id,
            "profile": {
                "id": self.profile.id,
                "caption": self.profile.caption,
                "age": self.profile.age,
                "gender": self.profile.gender,
                "city": self.profile.city,
                "occupation": self.profile.occupation,
                "income": self.profile.income,
                "ethnicity": self.profile.ethnicity,
                "account": {
                    "id": self.profile.account.id,
                    "username": self.profile.account.username,
                    "name": self.profile.account.name,
                    "email": self.profile.account.email,
                    "password": self.profile.account.password
                }
            }
        }
        
# File model has a many-to-1 relationship with Photo
class File(Base):
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    photo_id = Column(Integer, ForeignKey("photo.id"), nullable=False)
    
    # add the path property here? 
    def as_dictionary(self):
        return {
            "id": self.id,
            "name": self.name,
            "photo": {
                "id": self.photo.id,
                "profile": {
                    "id": self.photo.profile.id,
                    "caption": self.photo.profile.caption,
                    "age": self.photo.profile.age,
                    "gender": self.photo.profile.gender,
                    "city": self.photo.profile.city,
                    "occupation": self.photo.profile.occupation,
                    "income": self.photo.profile.income,
                    "ethnicity": self.photo.profile.ethnicity,
                    "account": {
                        "id": self.photo.profile.account.id,
                        "username": self.photo.profile.account.username,
                        "name": self.photo.profile.account.name,
                        "email": self.photo.profile.account.email,
                        "password": self.photo.profile.account.password
                    }
                }
            }
        }
        

        
