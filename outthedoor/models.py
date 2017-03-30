import os.path
import datetime

from flask import url_for
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from outthedoor import app
from .database import Base, engine

class Account(Base, UserMixin):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(128), nullable=False, unique=True)
    firstname = Column(String(128), nullable=False)
    lastname = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)

    posts = relationship("Post", uselist=False, backref="account")
    
    def as_dictionary(self):
        account = {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "password": self.password
        }
        return account

# Post model has a 1-to-1 relationship with Account, and a 1-to-1 relationship with Photo
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True)
    caption = Column(String(1024), nullable=False)
    age = Column(Integer, primary_key=False)
    gender = Column(String(1024))
    ethnicity = Column(String(1024))
    city = Column(String(1024))
    profession = Column(String(1024))
    income = Column(String(1024))
    datetime = Column(DateTime, default=datetime.datetime.now)
    
    account_id = Column(Integer, ForeignKey('accounts.id'))
    photo_id = Column(Integer, ForeignKey('photos.id'))
    
    def as_dictionary(self):
        post = {
            "id": self.id,
            "caption": self.caption,
            "age": self.age,
            "gender": self.gender,
            "ethnicity": self.ethnicity,
            "city": self.city,
            "profession": self.profession,
            "income": self.income,
            "account": self.account.as_dictionary(),
            "photo": self.photo.as_dictionary()
        }
        return post
        
class File(Base):
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    photos = relationship("Photo", uselist=False, backref="file")
    
    def as_dictionary(self):
        file = {
            "id": self.id,
            "name": self.name,
            "path": url_for("uploaded_file", name=self.name)
        }
        return file
        
class Photo(Base):
    __tablename__ = "photos"
    
    id = Column(Integer, primary_key=True)
    
    file_id = Column(Integer, ForeignKey('files.id'), nullable=False)
    
    posts = relationship("Post", uselist=False, backref="photo")
    
    def as_dictionary(self):
        photo = {
            "id": self.id,
            "file": self.file.as_dictionary()
        }
        return photo


Base.metadata.create_all(engine)
