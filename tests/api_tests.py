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
os.environ["CONFIG_PATH"] = "out_the_door.config.TestingConfig"

from out_the_door import app
from out_the_door import models
from out_the_door.utils import upload_path
from out_the_door.database import Base, engine, session
from out_the_door.models import Account, Profile, Photo, File

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
    
    # this test isn't even running   
    def create_profile(self):
        profileA = Profile(caption="What I bring with me everyday",
            age=25,
            gender="Female",
            city="Philadelphia",
            income="1000000",
            ethnicity="White"
        )
        
        profileA.account = self.account
        
        session.add(profileA)
        session.commit()
        
        return profileA
        
    # ACCOUNT TESTS 

    def test_account_get(self):
        pass
        
        
    def test_account_post(self):
        pass

    # # PROFILE TESTS 
    
    def test_profile_get_empty(self):
        """Get profiles from an empty profile database"""
        
        response = self.client.get("/api/profiles", headers=[("Accept", "application/json")])
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        
        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(data, [])
        
    def test_profile_get(self):
        """Get profiles from a populated database"""
        
        self.create_profile()
        
        response = self.client.get("/api/profiles", headers=[("Accept", "application/json")])
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        
        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(len(data), 1)
        
        profileA = data[0]
        self.assertEqual(profileA["caption"], "What I bring with me everyday")
        self.assertEqual(profileA["age"], 25)
        self.assertEqual(profileA["gender"], "Female")
        self.assertEqual(profileA["city"], "Philadelphia")
        self.assertEqual(profileA["income"], 1000000)
        self.assertEqual(profileA["ethnicity"], "White")
        self.assertEqual(profileA["account"]["username"], self.account.username)
        
        
    def test_profile_post(self):
        # self.simulate_login()
        pass
    
    # PHOTO TESTS 
    def test_photo_post(self):
        self.simulate_login()
        
        new_profile = self.create_profile()
        
        data = {
            "profile": {
                "id": new_profile.id
            }
        }

        response = self.client.post("/api/photos/",
            data=data,
            content_type="application/json",
            headers=[("Accept", "application/json")]
        )
        
        photos = session.query(Photo)
        
        self.assertEqual(len(photos), 1)
        
        
        
     
        
       
        
        
        
        
        
    
    # FILE TESTS 