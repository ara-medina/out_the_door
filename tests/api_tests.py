import unittest
import os
import shutil
import json
try: from urllib.parse import urlparse
except ImportError: from urlparse import urlparse # Py2 compatibility
from io import StringIO, BytesIO
from werkzeug.security import generate_password_hash
from flask_login import current_user

import sys; print(list(sys.modules.keys()))
# Configure the app to use the testing databse
os.environ["CONFIG_PATH"] = "outthedoor.config.TestingConfig"

from outthedoor import app
from outthedoor import models
from outthedoor.utils import upload_path
from outthedoor.database import Base, engine, session
from outthedoor.models import Post, Account

class TestAPI(unittest.TestCase):
    """Tests for the Out the Door API"""
    
    def setUp(self):
        """Test setup"""
        
        self.client = app.test_client()
        
        app.config['SECRET_KEY'] = 'your_secret_key_here'
        
        # Set up the tables in the database
        Base.metadata.create_all(engine)
        
        self.account = Account(username="sandramedina",
            firstname="Sandra", 
            lastname="Medina",
            email="sandra@example.com",
            password=generate_password_hash("test")
        )
        session.add(self.account)
        session.commit()

        # Create folder for test uploads
        # os.mkdir(upload_path())
        
    def tearDown(self):
        """Test teardown"""
        
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

        # Delete test upload folder
        # shutil.rmtree(upload_path())
        
    def simulate_login(self):
        with self.client.session_transaction() as http_session:
            http_session["user_id"] = str(self.account.id)
            http_session["_fresh"] = True
    
    def create_post(self):
        self.simulate_login()
        
        post = Post(caption="What I bring with me everyday")
        
        post.account = self.account
        
        session.add(post)
        session.commit()
        
        return post
        
    # # ACCOUNT TESTS 

    def test_account_get(self):
        
        account = Account(username="fernandomedina",
            firstname="Fernando",
            lastname="Medina",
            email="fernando@example.com",
            password=generate_password_hash("test"))
            
        session.add(account)
        session.commit()
        
        with self.client.session_transaction() as http_session:
            http_session["user_id"] = str(account.id)
            http_session["_fresh"] = True
        
        response = self.client.get("/api/accounts/{}".format(account.id), 
            headers=[("Accept", "application/json")])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data.decode("ascii"))
        
        account = data[0]
        self.assertEqual(account["username"], "fernandomedina")
        self.assertEqual(account["firstname"], "Fernando")
        self.assertEqual(account["lastname"], "Medina")
        self.assertEqual(account["email"], "fernando@example.com")
        
    def test_account_post(self):
        """ Creating a new account """

        data = {
            "username": "fernandomedina",
            "firstname": "Fernando",
            "lastname": "Medina",
            "email": "fernando@example.com",
            "password": generate_password_hash("test")
        }
        
        response = self.client.post("/api/accounts",
            data=json.dumps(data),
            content_type="application/json",
            headers=[("Accept", "application/json")]
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.mimetype, "application/json")

        self.assertEqual(data["username"], "fernandomedina")
        self.assertEqual(data["firstname"], "Fernando")
        self.assertEqual(data["lastname"], "Medina")
        self.assertEqual(data["email"], "fernando@example.com")

        accounts = session.query(models.Account).all()
        self.assertEqual(len(accounts), 2)

        account = accounts[1]
        self.assertEqual(account.username, "fernandomedina")
        self.assertEqual(account.firstname, "Fernando")
        self.assertEqual(account.lastname, "Medina")
        self.assertEqual(account.email, "fernando@example.com")

    # # # POST TESTS 
    
    def test_post_get_empty(self):
        """Get posts from an empty post database"""
        
        response = self.client.get("/api/posts", 
            headers=[("Accept", "application/json")])
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        
        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(data, [])
        
    def test_get_posts(self):
        """Get posts from a populated database"""
        
        self.create_post()
        
        response = self.client.get("/api/posts", 
            headers=[("Accept", "application/json")])
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        
        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(len(data), 1)
        
        postA = data[0]
        self.assertEqual(postA["caption"], "What I bring with me everyday")
        
    def test_get_single_post(self):
        """ Getting a single post from a populated database """

        postA = self.create_post()
        
        response = self.client.get("/api/posts/{}".format(postA.id), 
            headers=[("Accept", "application/json")])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data.decode("ascii"))
        
        postA = data
        self.assertEqual(postA["caption"], "What I bring with me everyday")
        
    def test_get_non_existent_post(self):
        """ Getting a single post which doesn't exist """
        
        response = self.client.get("/api/posts/1", 
            headers=[("Accept", "application/json")])

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(data["message"], "Could not find post with id 1")
        
    def test_unsupported_accept_header(self):
        """ Recieving an unsupported accept header """ 
        
        response = self.client.get("/api/posts",
            headers=[("Accept", "application/xml")]
        )

        self.assertEqual(response.status_code, 406)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(data["message"],
                         "Request must accept application/json data")
                         
    def test_delete_entry(self):
        """ Delete a single post """
        
        self.simulate_login()
        
        postA = self.create_post()
        
        response = self.client.delete("/api/posts/{}".format(postA.id), 
            content_type="application/json",
            headers=[("Accept", "application/json")])
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        self.assertEqual(urlparse(response.location).path, "/api/posts")
        
        post = json.loads(response.data.decode("ascii"))
        
        posts = session.query(Post).all()
        
        self.assertEqual(len(posts), 0)
        self.assertEqual(post, [])

        
    def test_post_post(self):
        """ Posting a new post """
        
        self.simulate_login()
        
        data = {
            "caption": "What I bring",
            "age": 100,
            "gender": "Male",
            "ethnicity": "Hispanic",
            "city": "Boston",
            "profession": "Doctor",
            "income": 3000000,
            "account": self.account.as_dictionary()
        }
        
        response = self.client.post("/api/posts",
            data=json.dumps(data),
            content_type="application/json",
            headers=[("Accept", "application/json")]
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.mimetype, "application/json")
        self.assertEqual(urlparse(response.headers.get("Location")).path,
                         "/api/posts/1")

        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["caption"], "What I bring")
        self.assertEqual(data["age"], 100)

        posts = session.query(models.Post).all()
        self.assertEqual(len(posts), 1)

        post = posts[0]
        self.assertEqual(post.caption, "What I bring")
        self.assertEqual(post.account, self.account)
        
    def test_edit_post(self):
        self.simulate_login()
        
        post = Post(caption="What I bring",
            age=25,
            gender="Female",
            ethnicity="White",
            city="Seattle",
            profession="Developer",
            income=10000000,
            account=self.account)
 
        session.add(post)
        session.commit()
        
        data = {
            "caption": "New What I bring",
            "age": 25,
            "gender": "Female",
            "ethnicity": "White",
            "city": "Seattle",
            "profession": "Developer",
            "income": 10000000,
            "account": self.account.as_dictionary()
        }
        
        response = self.client.post("/api/post/{}/edit".format(post.id), 
            data=json.dumps(data), 
            content_type="application/json", 
            headers=[("Accept", "application/json")])
        
        edited_post = session.query(Post).get(post.id)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(edited_post.caption, "New What I bring")
        self.assertEqual(post.account, self.account)
        
        self.assertEqual(session.query(Post).count(), 1)
    
    # # FILE TESTS 
    
    # # PHOTO TESTS 
      
        
        
     
        
       
        
        
        
        
        
    
    