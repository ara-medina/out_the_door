from flask_login import LoginManager

from . import app
from .database import session
from .models import Account, Post, Photo, File

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_message_category = "danger"


@login_manager.user_loader
def load_account(id):
    return session.query(Account).get(int(id))