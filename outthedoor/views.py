from flask import render_template

from outthedoor import app

@app.route("/")
def index():
    return app.send_static_file("index.html")