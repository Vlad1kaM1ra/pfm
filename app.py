import os
from flask import Flask, session, request, jsonify
from flask_session import Session
from tempfile import mkdtemp
from flask import render_template
from helpers import apology
from werkzeug.exceptions import default_exceptions
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/')
def index():
    User.add_user(User, email="test@gmail.com", hashstring="testhash1")
    return render_template("index.html")


@app.route('/signup', methods=["GET", "POST"])
def signup():
    return render_template("signup.html")


@app.route('/check_user', methods=["GET"])
def check_user():
    """
    Check user existence by email
    :return:
    True or False
    """
    email = request.args.get("email")
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(True)
    else:
        return jsonify(False)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


if __name__ == '__main__':
    app.run()
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
