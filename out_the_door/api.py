import json

from flask import request, Response, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

from . import models
from . import decorators
from out_the_door import app
from .database import session
from .models import Account, Profile, Photo, File
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

@app.route("/api/accounts", methods=["GET"])
@decorators.accept("application/json")
def account_get():
    """Get a set of accounts"""
    
    accounts = session.query(Account)
    accounts = accounts.order_by(Account.id)
    
    data = json.dumps([account.as_dictionary() for account in accounts])
    return Response(data, 200, mimetype="application/json")

# does this require a require decorator? 
@app.route("/api/accounts", methods=["POST"])
@decorators.accept("application/json")
def account_post():
    """Create a new account"""
    pass

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
    
    # is this really being accessed correctly?
    id = data["profile"]["account"]["id"]
    account = session.query(Account).get(id)
    
    # double check this
    profile = Profile(caption=data["profile"]["caption"],
        age=data["profile"]["age"],
        gender=data["profile"]["gender"],
        city=data["profile"]["city"],
        occupation=data["profile"]["occupation"],
        income=data["profile"]["income"],
        ethnicity=data["profile"]["ethnicity"],
        account=account)
    session.add(profile)
    session.commit()
    
    data = json.dumps(profile.as_dictionary())
    return Response(data, 201, mimetype="application/json")
    
@app.route("/uploads/<name>", methods=["GET"])
def uploaded_file(name):
    """Retrieve an uploaded file"""
    return send_from_directory(upload_path(), name)
    
@app.route("/api/files", methods=["POST"])
@decorators.require("multipart/form-data")
@decorators.accept("application/json")
def file_post():
    """Post an uploaded file to the database"""
    # get the uploaded file; return an error if not found 
    file = request.files.get("file")
    if not file:
        data = {"message": "Could not find file data"}
        return Response(json.dumps(data), 422, mimetype="application/json")

    # give the file a safe name
    name = secure_filename(file.filename)
    # create a File object and add it to the db
    new_file = File(name=name)
    session.add(new_file)
    session.commit()
    # save the file to an uploads folder
    file.save(upload_path(name))

    data = new_file.as_dictionary()
    return Response(json.dumps(data), 201, mimetype="application/json")
    

