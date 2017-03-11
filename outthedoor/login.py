from flask_login import LoginManager

from . import app
from .database import session
from .models import Account, Post

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "/api/accounts" #not totally sure this will work so come back to it
login_manager.login_message_category = "danger"


@login_manager.user_loader
def load_account(id):
    return session.query(Account).get(int(id))