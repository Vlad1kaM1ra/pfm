from flask import Flask
from flask import render_template
from helpers import apology
from werkzeug.exceptions import default_exceptions

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signup')
def signup():
    return render_template("signup.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)




if __name__ == '__main__':
    app.run()
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)