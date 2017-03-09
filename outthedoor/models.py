import os.path
import datetime

from flask import url_for
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship

from outthedoor import app
from .database import Base, engine

# class Account(Base, UserMixin):
#     __tablename__ = "accounts"
    
#     id = Column(Integer, primary_key=True)
#     username = Column(String(128), nullable=False, unique=True)
#     name = Column(String(128), nullable=False)
#     email = Column(String(128), nullable=False, unique=True)
#     password = Column(String(128), nullable=False)

#     posts = relationship("Post", uselist=False, backref="account")
    
#     def as_dictionary(self):
#         account = {
#             "id": self.id,
#             "username": self.username,
#             "name": self.name,
#             "email": self.email,
#             "password": self.password
#         }
#         return account

# Post model has a 1-to-1 relationship with Account, and a 1-to-many relationship with Photo
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True)
    caption = Column(String(1024))
    datetime = Column(DateTime, default=datetime.datetime.now)
    
    # account_id = Column(Integer, ForeignKey('accounts.id'))
    
    # photos = relationship("Photo", backref="profile")
    
    def as_dictionary(self):
        post = {
            "id": self.id,
            "caption": self.caption
            # "account": self.account.as_dictionary()
        }
        return post
        
# # File model has a 1-to-1 relationship with Photo
# class File(Base):
#     __tablename__ = "files"
    
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
    
#     photo = relationship("Photo", uselist=False, backref="file")
    
#     def as_dictionary(self):
#         return {
#             "id": self.id,
#             "name": self.name
#             # "photo": self.photo.as_dictionary()
#         }
        
# # Photo model has a many-to-1 relationship with Profile, and a 1-to-1 relationship with File
# class Photo(Base):
#     __tablename__ = "photos"
    
#     id = Column(Integer, primary_key=True)
    
#     profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
#     file_id = Column(Integer, ForeignKey("files.id"), nullable=False)
    
#     def as_dictionary(self):
#         return {
#             "id": self.id,
#             "profile": self.profile.as_dictionary(),
#             "file": self.file.as_dictionary()
#         }


Base.metadata.create_all(engine)
