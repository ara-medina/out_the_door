import os
    
class DevelopmentConfig(object):
    # DATABASE_URI = os.environ.get('DATABASE_URL') make this work later
    DATABASE_URI = "postgres://rynrlowmlmimbg:87da8ff0d29f3aa2cf70ff197c2a36d453d4bfea736db3f7d4f945abb88ab6fb@ec2-23-23-93-255.compute-1.amazonaws.com:5432/d3u3k598il0j99"
    DEBUG = True
    UPLOAD_FOLDER = "uploads"
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    SECRET_KEY = os.environ.get("OUTTHEDOOR_SECRET_KEY", os.urandom(12))
    FLASKS3_BUCKET_NAME = 'mybucketname'

class TestingConfig(object):
    DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/outthedoor-test"
    DEBUG = True
    UPLOAD_FOLDER = "test-uploads"
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    SECRET_KEY = os.environ.get("OUTTHEDOOR_SECRET_KEY", os.urandom(12))