import os
from getpass import getpass
from werkzeug.security import generate_password_hash

from outthedoor import app
from outthedoor.database import session, Post, Account

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def seed():
    for i in range(25):
        post = Post(
            caption="Test Post #{}".format(i)
        )
        session.add(post)
    session.commit()
    
def addaccount():
    username = input("Username: ")
    name = input("Name: ")
    email = input("Email: ")
    if session.query(Account).filter_by(email=email).first():
        print("Account with that email address already exists")
        return

    password = ""
    while len(password) < 8 or password != password_2:
        password = getpass("Password: ")
        password_2 = getpass("Re-enter password: ")
    account = Account(username=username, name=name, email=email,
                password=generate_password_hash(password))
    session.add(account)
    session.commit()
    

if __name__ == "__main__":
    run()
