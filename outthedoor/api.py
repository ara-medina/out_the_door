import os, boto3, json

from flask import Flask

from flask import request, Response, url_for, redirect, render_template, send_from_directory, flash
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask_login import login_required
from getpass import getpass

from outthedoor import app
from . import models
from . import decorators
from .database import session
from .models import Post, Account, Photo, File
# from .utils import upload_path
from .config import TestingConfig


post_schema = {
    "properties": {
        "caption": {"type": "string"},
        "age": {"type": "number"},
        "gender": {"type": "string"},
        "ethnicity": {"type": "string"},
        "city": {"type": "string"},
        "profession": {"type": "string"},
        "account": {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "firstname": {"type": "string"},
                "lastname": {"type": "string"},
                "email": {"type": "string"},
                "password": {"type": "string"}
            }
        },
        "photo": {
            "type": "object",
            "properties": {
                "file" : {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "path": {"type": "string"}
                        
                    }
                }
            }
        }
    }
}

# ACCOUNT ENDPOINTS 

@app.route("/api/accounts/<int:id>", methods=["GET"])
@decorators.accept("application/json")
def account_get(id):
    """Get a single account"""
    account = session.query(Account).get(id)
    
    if not account:
        message = "Could not find account with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")
    
    data = json.dumps([account.as_dictionary()])
    return Response(data, 200, mimetype="application/json")

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
        
    username_taken = session.query(Account).filter_by(username=data['username']).first()
    email_taken  = session.query(Account).filter_by(email=data['email']).first()
    
    if username_taken:
        data = "This username is already taken. Please pick a new username."
        return Response(data, 400, mimetype="application/json")
    elif email_taken:
        data = "This email address is already in use. Please provide a different email address."
        return Response(data, 400, mimetype="application/json")
    else:
        account = Account(username=data["username"],
            firstname=data["firstname"],
            lastname=data["lastname"],
            email=data["email"],
            password=generate_password_hash(data["password"]))
        session.add(account)
        session.commit()
        
        data = json.dumps(account.as_dictionary())
        headers = {"Location": url_for("posts_get")}
        return Response(data, 201, headers=headers,
                        mimetype="application/json")

@app.route("/api/login", methods=["POST"])
def login_post():
    data = request.json
    
    username = data["username"]
    password = data["password"]
    
    # check that username exists
    account = session.query(Account).filter_by(username=username).first()
    
    if not account or not check_password_hash(account.password, password):
        data = "Incorrect username or password"
        return Response(data, 400, mimetype="application/json")
    
    # if the user has previously posted, find the post that is associated with the account
    if account.posts:
        post = account.posts
        post = post.as_dictionary()
    
        # add that post to the data dictionary
        data["post"] = post

    login_user(account)
    
    data = json.dumps(data)
    headers = {"Location": url_for("posts_get")}
    return Response(data, 201, headers=headers,
                    mimetype="application/json")

@app.route("/api/logout")
def logout():
    logout_user()
    
    data = json.dumps([])
    headers = {"Location": url_for("posts_get")}
    return Response(data, 200, headers=headers,
                    mimetype="application/json")

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
    print(data)

    id = data["photo"]["id"]
    photo = session.query(Photo).get(id)
    
    try: 
        validate(data, post_schema)
        print("validated")
    except ValidationError as error:
        data = {"message": error.message}
        print("not validated")
        return Response(json.dumps(data), 422, mimetype="application/json")
        
    post = Post(caption=data["caption"], 
        age=data["age"],
        gender=data["gender"],
        ethnicity=data["ethnicity"],
        city=data["city"],
        profession=data["profession"],
        account=current_user,
        photo=photo)
        
    print(post)
        
    session.add(post)
    session.commit()

    data = json.dumps(post.as_dictionary())
    headers = {"Location": url_for("post_get", id=post.id)}
    return Response(data, 201, headers=headers,
                    mimetype="application/json")

@app.route("/api/post/<id>/edit", methods=["POST"])
@decorators.accept("application/json")
@decorators.require("application/json")
def posts_edit(id):
    """Edit a post"""
    data = request.json
    print(data)
    
    try: 
        validate(data, post_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")
        
    photoId = data["photo"]["id"]
    photo = session.query(Photo).get(photoId)
        
    post = session.query(Post).get(id)
    post.caption = data["caption"]
    post.age = data["age"]
    post.gender = data["gender"]
    post.ethnicity = data["ethnicity"]
    post.city = data["city"]
    post.profession = data["profession"]
    post.photo = photo
    
    session.commit()
    
    data = json.dumps(post.as_dictionary())
    headers = {"Location": url_for("posts_get")}
    return Response(data, 201, headers=headers, 
        mimetype="application/json")
        
# FILE ENDPOINTS
def allowed_file(filename):
    print("testing filename extension")
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in TestingConfig.ALLOWED_EXTENSIONS
           
@app.route('/sign_s3/', methods=["GET"])
def sign_s3():
    S3_BUCKET = os.environ.get('S3_BUCKET')
    
    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')
    
    s3 = boto3.client('s3')
    
    presigned_post = s3.generate_presigned_post(
    Bucket = S3_BUCKET,
    Key = file_name,
    Fields = {"acl": "public-read", "Content-Type": file_type},
    Conditions = [
      {"acl": "public-read"},
      {"Content-Type": file_type}
    ],
    ExpiresIn = 3600
    )
    
    return json.dumps({
        'data': presigned_post,
        'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
    })
           
@app.route("/api/files", methods=["POST"])
@decorators.require("multipart/form-data")
@decorators.accept("application/json")
def file_post():
    """Post an uploaded file to the database"""
    
    # get the uploaded file; return an error if not found 
    file = request.files.get("file")
    print("printing file")
    print(file)
    if not file:
        data = {"message": "Could not find file data"}
        return Response(json.dumps(data), 422, mimetype="application/json")
        
    allowed_file(file.filename)

    # give the file a safe name
    name = secure_filename(file.filename)
    
    # create a File object and add it to the db
    new_file = File(name=name)
    session.add(new_file)
    print("printing new_file")
    print(new_file.as_dictionary())
    session.commit()
    
    # save the file to an uploads folder
    # file.save(upload_path(name))

    data = new_file.as_dictionary()
    return Response(json.dumps(data), 201, mimetype="application/json")
           
# PHOTO ENDPOINTS
@app.route("/api/photos", methods=["GET"])
@decorators.accept("application/json")
def photos_get():
    """Get a list of photos"""
    
    photos = session.query(Photo)
    photos = photos.order_by(Photo.id)
    print(photos)
    
    data = json.dumps([photo.as_dictionary() for photo in photos])
    return Response(data, 200, mimetype="application/json")
    
@app.route("/api/photos/<int:id>", methods=["GET"])
@decorators.accept("application/json")
def photo_get(id):
    """Get a single photo"""
    
    photo = session.query(Photo).get(id)
    
    if not photo:
        message = "Could not find photo with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")
    
    data = json.dumps([photo.as_dictionary()])
    return Response(data, 200, mimetype="application/json")

    
@app.route("/api/photos", methods=["POST"])
@decorators.accept("application/json")
def photo_post():
    """Add a new photo"""
    data = request.json
    print("printing data")
    print(data)
    
    try: 
        validate(data, post_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")
        
    id = data["file"]["id"]
    file = session.query(File).get(id)
    print("printing file")
    print(file)
    
    photo = Photo(file=file)
    session.add(photo)
    session.commit()
    print("printing photo")
    print(photo.as_dictionary())
    print("photo commit successful")
    
    data = json.dumps(photo.as_dictionary())
    return Response(data, 201, mimetype="application/json")
    
@app.route("/api/photos/<id>/edit", methods=["POST"])
@decorators.accept("application/json")
def photo_edit(id):
    """Edit a photo"""
    data = request.json
    
    try: 
        validate(data, post_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")
    
    # fix this
    photo = session.query(Photo).get(id)
    photo.file = data["file"]
    photo.post = data["post"]
    
    session.commit()
    
    data = json.dumps(photo.as_dictionary())
    headers = {"Location": url_for("posts_get")}
    return Response(data, 201, headers=headers, 
        mimetype="application/json")
        
@app.route("/api/photos/<int:id>", methods=["DELETE"])
@decorators.accept("application/json")
def delete_photo(id):
    photo = session.query(Photo).get(id)
    
    if not photo:
        message = "Could not find photo with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    session.delete(photo)
    session.commit()

    data = json.dumps([])
    headers = {"Location": url_for("posts_get")}
    return Response(data, 200, headers=headers,
                    mimetype="application/json")
    
    
# # UPLOAD ENDPOINTS
# @app.route("/uploads/<name>", methods=["GET"])
# def uploaded_file(name):
#     """Retrieve an uploaded file"""
#     return send_from_directory(upload_path(), name)
    

    

