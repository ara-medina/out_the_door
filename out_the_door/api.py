import json

from flask import request, Response, url_for, render_template
from jsonschema import validate, ValidationError

from . import models
# from . import decorators
from out_the_door import app
from .database import session
from .models import Account, Profile
from .utils import upload_path

profile_schema = {
    "properties": {
        "caption": {"type": "string"},
        "age": {"type": "integer"},
        "gender": {"type": "string"},
        "city": {"type": "string"},
        "occupation": {"type": "string"},
        "income": {"type": "string"},
        "ethnicity": {"type": "string"},
        "accounts": {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "name": {"type": "string"},
                "email": {"type": "string"},
                "password": {"type": "string"}
            }
        }
    }
}

@app.route("/api/profiles", methods=["GET"])
# @decorators.accept("application/json")
def profiles_get():
    """Get a set of profiles"""
    
    profiles = session.query(Profile)
    profiles = profiles.order_by(Profile.id)
    
    data = json.dumps([profile.as_dictionary() for profile in profiles])
    return Response(data, 200, mimetype="application/json")
    

# this needs to check to see if the person has made a profile yet and gives them an error if they have
# @app.route("/api/profiles", methods=["GET"])
# # @login_required
# def add_profile_get():
#     return render_template("add_profile.html")
    
@app.route("/api/profiles", methods=["POST"])
# @login_required
def add_profile_post():
    profile = Profile(
        caption = request.form["caption"],
        age = request.form["age"],
        gender = request.form["gender"],
        city = request.form["city"],
        occupation = request.form["occupation"],
        income = request.form["income"],
        ethnicity = request.form["ethnicity"]
    )
    session.add(profile)
    session.commit()
    # return redirect(url_for("entries"))
