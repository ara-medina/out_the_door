import os

class DevelopmentConfig(object):
    DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/outthedoor"
    DEBUG = True
    # UPLOAD_FOLDER = "uploads"
    # SECRET_KEY = os.environ.get("OUTTHEDOOR_SECRET_KEY", os.urandom(12))

class TestingConfig(object):
    DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/outthedoor-test"
    DEBUG = True
    # UPLOAD_FOLDER = "test-uploads"
    # SECRET_KEY = os.environ.get("OUTTHEDOOR_SECRET_KEY", os.urandom(12))