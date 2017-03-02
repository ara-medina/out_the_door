import json

from flask import Flask

from flask import request, Response, url_for, redirect, render_template, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError
from werkzeug.security import check_password_hash
from flask_login import LoginManager
from flask_login import login_required
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user

from outthedoor import app
from . import models
from . import decorators
from .database import session
from .models import Account, Post
from .utils import upload_path

post_schema = {
    "properties": {
        "caption": {"type": "string"},
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

# ACCOUNT ENDPOINTS 

# @app.route("/api/accounts", methods=["GET"])
# @decorators.accept("application/json")
# def account_get():
#     """Get a set of accounts"""
    
#     accounts = session.query(Account)
#     accounts = accounts.order_by(Account.id)
    
#     data = json.dumps([account.as_dictionary() for account in accounts])
#     return Response(data, 200, mimetype="application/json")

@app.route("/api/accounts", methods=["POST"])
@decorators.accept("application/json")
def account_post():
    """Create a new account"""
    data = request.json
    
    try:
        validate(data, post_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")
        
    account = Account(username=data["account"]["username"],
        name=data["account"]["name"],
        email=data["account"]["email"],
        password=data["account"]["password"])
    session.add(account)
    session.commit()
    
    data = json.dumps(account.as_dictionary())
    return Response(data, 201, mimetype="application/json")
    
# @app.route('/api/users', methods = ['POST'])  should this replace the previous route ? 
# def new_user():
#     username = request.json.get('username')
#     password = request.json.get('password')
#     if username is None or password is None:
#         abort(400) # missing arguments
#     if User.query.filter_by(username = username).first() is not None:
#         abort(400) # existing user
#     user = User(username = username)
#     user.hash_password(password)
#     db.session.add(user)
#     db.session.commit()
#     return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}
    
    
@app.route("/api/accounts/<int:id>", methods=["GET"])
@decorators.accept("application/json")
def get_account(id):
    """Get a specific user account"""
    
    account = session.query(Account).get(id)
    
    data = json.dumps(account.as_dictionary())
    return Response(data, 200, mimetype="application/json")
    
# # POST ENDPOINTS 
@app.route("/api/posts", methods=["GET"])
@decorators.accept("application/json")
def posts_get():
    """Get a set of posts"""
    
    posts = session.query(Post)
    post = posts.order_by(Post.id)
    
    data = json.dumps([post.as_dictionary() for post in posts])
    return Response(data, 200, mimetype="application/json")
    
@app.route("/api/posts/<int:id>", methods=["GET"])
@decorators.accept("application/json")
def post_get(id):
    """ Single post endpoint """
    
    post = session.query(Post).get(id)

    if not post:
        message = "Could not find post with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    data = json.dumps(post.as_dictionary())
    return Response(data, 200, mimetype="application/json")
    
@app.route("/api/posts/<int:id>", methods=["DELETE"])
@decorators.accept("application/json")
def delete_post(id):
    post = session.query(Post).get(id)
    
    if not post:
        message = "Could not find post with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    session.delete(post)
    session.commit()

    data = json.dumps([])
    headers = {"Location": url_for("posts_get")}
    return Response(data, 200, headers=headers,
                    mimetype="application/json")
    
@app.route("/api/posts", methods=["POST"])
@decorators.accept("application/json")
@decorators.require("application/json")
def posts_post():
    """ Add a new post """
    data = request.json
    
    try: 
        validate(data, post_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")
    
    id = data["account"]["id"]
    account = session.query(Account).get(id)

    post = Post(caption=data["caption"], account=account)
    session.add(post)
    session.commit()

    data = json.dumps(post.as_dictionary())
    headers = {"Location": url_for("post_get", id=post.id)}
    return Response(data, 201, headers=headers,
                    mimetype="application/json")

@app.route("/api/post/<id>", methods=["POST"])
@decorators.accept("application/json")
@decorators.require("application/json")
def posts_edit(id):
    """Edit a post"""
    data = request.json
    
    try: 
        validate(data, post_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")
        
    post = session.query(Post).get(id)
    post.caption = data["caption"]
    
    session.commit()
    
    data = json.dumps(post.as_dictionary())
    headers = {"Location": url_for("post_get", id=post.id)}
    return Response(data, 201, headers=headers, 
        mimetype="application/json")
    
    
# # PHOTO ENDPOINTS
# @app.route("/api/photos", methods=["GET"])
# @decorators.accept("application/json")
# def photo_get():
#     """Get a set of photos"""
    
#     photos = session.query(Photo)
#     photos = photos.order_by(Photo.id)
    
#     data = json.dumps([photo.as_dictionary() for photo in photos])
#     return Response(data, 200, mimetype="application/json")
    
# @app.route("/api/photos", methods=["POST"])
# @decorators.accept("application/json")
# @login_required
# def photo_post():
#     """Post a new photo"""
    
#     data = request.json
    
#     profile_id = data["profile"]["id"]
#     file_id = data["file"]["id"]
#     profile = session.query(Profile).get(id)
#     file = session.query(File).get(id)
    
#     photo = Photo(profile=profile, file=file)
#     session.add(photo)
#     session.commit()
    
#     data = json.dumps(photo.as_dictionary())
#     return Response(data, 201, mimetype="application/json")
    
# # FILE ENDPOINTS
# @app.route("/api/files", methods=["GET"])
# @decorators.accept("application/json")
# def file_get():
#     """Get files that have been uploaded"""
    
#     files = session.query(File)
#     files = files.order_by(id)
    
#     data = json.dumps([file.as_dictionary() for file in files])
#     return Response(data, 200, mimetype="application/json")
    
# @app.route("/api/files", methods=["POST"])
# @decorators.require("multipart/form-data")
# @decorators.accept("application/json")
# @login_required
# def file_post():
#     """Post an uploaded file to the database"""
#     # get the uploaded file; return an error if not found 
#     file = request.files.get("file")
#     if not file:
#         data = {"message": "Could not find file data"}
#         return Response(json.dumps(data), 422, mimetype="application/json")

#     # give the file a safe name
#     name = secure_filename(file.filename)
#     # create a File object and add it to the db
#     new_file = File(name=name)
#     session.add(new_file)
#     session.commit()
#     # save the file to an uploads folder
#     file.save(upload_path(name))

#     data = new_file.as_dictionary()
#     return Response(json.dumps(data), 201, mimetype="application/json")
    
# # UPLOAD ENDPOINTS
# # does this need a decorator?
# @app.route("/uploads/<name>", methods=["GET"])
# def uploaded_file(name):
#     """Retrieve an uploaded file"""
#     return send_from_directory(upload_path(), name)
    

    
