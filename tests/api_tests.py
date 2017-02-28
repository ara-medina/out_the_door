import unittest
import os
import shutil
import json
try: from urllib.parse import urlparse
except ImportError: from urlparse import urlparse # Py2 compatibility
from io import StringIO, BytesIO
from werkzeug.security import generate_password_hash

import sys; print(list(sys.modules.keys()))
# Configure the app to use the testing databse
os.environ["CONFIG_PATH"] = "outthedoor.config.TestingConfig"

from outthedoor import app
from outthedoor import models
from outthedoor.utils import upload_path
from outthedoor.database import Base, engine, session
from outthedoor.models import Account, Post

class TestAPI(unittest.TestCase):
    """Tests for the Out the Door API"""
    
    def setUp(self):
        """Test setup"""
        
        self.client = app.test_client()
        
        app.config['SECRET_KEY'] = 'secret?'
        
        # Set up the tables in the database
        Base.metadata.create_all(engine)
        
        self.account = Account(name="Sandra", 
            username="sandramedina", 
            email="sandra@example.com",
            password=generate_password_hash("test")
        )
        session.add(self.account)
        session.commit()
        
        with self.client.session_transaction() as http_session:
            http_session["account_id"] = str(Account.id)
            http_session["_fresh"] = True

        # Create folder for test uploads
        os.mkdir(upload_path())
        
    def tearDown(self):
        """Test teardown"""
        
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

        # Delete test upload folder
        shutil.rmtree(upload_path())
        
    def simulate_login(self):
        with self.client.session_transaction() as http_session:
            http_session["account_id"] = str(self.account.id)
            http_session["_fresh"] = True
    
    def create_post(self):
        post = Post(caption="What I bring with me everyday")
        
        post.account = self.account
        
        session.add(post)
        session.commit()
        
        return post
        
    # # ACCOUNT TESTS 

    # def test_account_get(self):
    #     pass
        
        
    # def test_account_post(self):
    #     pass

    # # # PROFILE TESTS 
    
    def test_post_get_empty(self):
        """Get posts from an empty post database"""
        
        response = self.client.get("/api/posts", headers=[("Accept", "application/json")])
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        
        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(data, [])
        
    def test_get_posts(self):
        """Get posts from a populated database"""
        
        self.create_post()
        
        response = self.client.get("/api/posts", headers=[("Accept", "application/json")])
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        
        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(len(data), 1)
        
        postA = data[0]
        self.assertEqual(postA["caption"], "What I bring with me everyday")
        self.assertEqual(postA["account"]["username"], self.account.username)
        
    def test_get_single_post(self):
        """ Getting a single post from a populated database """

        postA = self.create_post()
        
        response = self.client.get("/api/posts/{}".format(postA.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data.decode("ascii"))
        
        postA = data
        self.assertEqual(postA["caption"], "What I bring with me everyday")
        
    def test_get_non_existent_post(self):
        """ Getting a single post which doesn't exist """
        
        response = self.client.get("/api/posts/1")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(data["message"], "Could not find post with id 1")
        
        
    # def test_profile_post(self):
    #     # self.simulate_login()
    #     pass
    
    # # FILE TESTS 
    
    # # PHOTO TESTS 
    # def test_photo_post(self):
    #     pass
      
        
        
     
        
       
        
        
        
        
        
    
    