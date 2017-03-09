import os
from getpass import getpass
from werkzeug.security import generate_password_hash

from outthedoor import app
from outthedoor.database import session
from outthedoor.models import Post

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    run()
