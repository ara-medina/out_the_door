import json

from flask import request, Response, url_for, render_template
from jsonschema import validate, ValidationError

from . import models
from . import decorators
from out_the_door import app
from .database import session
from .models import Account, Profile, Photo, File
# from .utils import upload_path

profile_schema = {
    "properties": {
        "caption": {"type": "string"},
        "age": {"type": "integer"},
        "gender": {"type": "string"},
        "city": {"type": "string"},
        "occupation": {"type": "string"},
        "income": {"type": "string"},
        "ethnicity": {"type": "string"},
        "account": {
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
@decorators.accept("application/json")
def profile_get():
    """Get a set of profiles"""
    
    profiles = session.query(Profile)
    profiles = profiles.order_by(Profile.id)
    
    data = json.dumps([profile.as_dictionary() for profile in profiles])
    return Response(data, 200, mimetype="application/json")
    

@app.route("/api/profiles", methods=["POST"])
@decorators.accept("application/json")
def profile_post():
    """Adds a new profile"""
    data = request.json
    
    try: 
        validate(data, profile_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")
    
    id = data["account"]["id"]
    account = session.query(Account).get(id)
    
    # does this need more properties?
    profile = Profile(account=account)
    session.add(profile)
    session.commit()
    
    data = json.dumps(profile.as_dictionary())
    return Response(data, 201, mimetype="application/json")
    
# an uploads endpoint here?
# @app.route("/uploads/<name>", methods=["GET"])
    
# a POST request here to handle the uploads?
