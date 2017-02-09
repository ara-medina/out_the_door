import os

from getpass import getpass
from werkzeug.security import generate_password_hash
from .database import Account, session, Base

from out_the_door import app

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    
def addaccount():
    name = input("Name: ")
    email = input("Email: ")
    if session.query(Account).filter_by(email=email).first():
        print("User with that email address already exists")
        return

    password = ""
    while len(password) < 8 or password != password_2:
        password = getpass("Password: ")
        password_2 = getpass("Re-enter password: ")
    account = Account(name=name, email=email,
                password=generate_password_hash(password))
    session.add(account)
    session.commit()
    
if __name__ == '__main__':
    run()
