from flask import render_template
from .database import session
from .models import Profile

from . import app

@app.route("/", methods=["GET"])
def profiles():
    profiles = session.query(Profile)
    profiles = profiles.order_by(Profile.datetime.desc())
    profiles = profiles.all()
    return render_template("profiles.html",
        profiles=profiles
    )