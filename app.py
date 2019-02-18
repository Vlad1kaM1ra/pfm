import os
import io
import csv
from flask import Flask, session, request, jsonify, redirect
from flask import render_template, make_response
from helpers import *
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
# app.config["SESSION_FILE_DIR"] = mkdtemp()
# app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "memcached"


# Set the secret key to some random bytes. Keep this really secret!
# Session(app)


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """
    Application main page
    """
    # get current user
    user = User.query.filter_by(id=session["user_id"]).first()
    expendituresData, expendituresSum = currentMonthExpenditureSummary(user)
    incomes, incomesTotal = currentMonthIncomeSummary(user)
    balance = incomesTotal - expendituresSum

    return render_template(
        "index.html",
        expendituresData=expendituresData,
        expendituresSum=expendituresSum,
        incomes=incomes,
        incomesTotal=incomesTotal,
        balance=balance)


# expenditure input main page controller
@app.route("/expinputmain")
@login_required
def expinputmain():
    # get current user
    user = User.query.filter_by(id=session["user_id"]).first()
    expendituresData, expendituresSum = currentMonthExpenditureSummary(user)

    return render_template(
        "expinputmain.html",
        expendituresData=expendituresData,
        expendituresSum=expendituresSum)


# income input main page controller
@app.route("/incomeinputmain", methods=["GET", "POST"])
@login_required
def incomeinputmain():
    # get current user
    user = User.query.filter_by(id=session["user_id"]).first()

    if request.method == "POST":
        date = request.form.get('date')
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        type = request.form.get('type')
        value = request.form.get('value')
        if not type or not value:
            return apology("Not provided type or value", 403)
        Income.add_income(Income, user, date, type, value)
        return redirect("/incomeinputmain")
    else:
        incomes, incomesTotal = currentMonthIncomeSummary(user)

        return render_template(
            "incomeinputmain.html",
            incomes=incomes,
            incomesTotal=incomesTotal)


@app.route("/incomedelete", methods=["POST"])
@login_required
def incomedelete():
    # get current user
    id = request.form.get("id")
    Income.del_income(Income, id)
    return redirect("/incomeinputmain")


# input expenditures items to concrete category
@app.route("/expinputcat", methods=["POST"])
@login_required
def expinputcat():
    names = request.form.getlist('name[]')
    prices = request.form.getlist('price[]')
    categoryName = request.form.get('category')
    dates = request.form.get('date')
    date = datetime.datetime.strptime(dates, '%Y-%m-%d').date()
    user = User.query.filter_by(id=session["user_id"]).first()
    category = Category.query.filter_by(name=categoryName).first()

    for i in range(len(names)):
        if not names[i] or not prices[i]:
            return apology("Not provided name or price", 403)
        Expenditure.add_expenditure(Expenditure, user, category, date, names[i], prices[i])
    return redirect("/expeditcat?category=" + categoryName + "&date=" + dates)


# edit expenditure page controller
@app.route("/expeditcat", methods=["GET"])
@login_required
def expeditcat():
    user = User.query.filter_by(id=session["user_id"]).first()
    categoryName = request.args.get("category")
    date = request.args.get("date")
    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    category = Category.query.filter_by(name=categoryName).first()
    expendituresData, expendituresSum = expenditureSummary(user, date, category)
    return render_template(
        "expeditcat.html",
        expendituresData=expendituresData,
        categoryName=categoryName,
        expendituresSum=expendituresSum
    )


# delete expenditure end point
@app.route("/delexpenditure", methods=["POST"])
@login_required
def delexpenditure():
    date = request.form.get("date")
    category = request.form.get("category")
    expenditureId = request.form.get("id")

    Expenditure.del_expenditure(Expenditure, expenditureId)

    return redirect("/expeditcat?category=" + category + "&date=" + date)


@app.route("/expreview", methods=["GET", "POST"])
@login_required
def expreview():
    user = User.query.filter_by(id=session["user_id"]).first()
    begin = request.form.get("startdate")
    end = request.form.get("enddate")
    expendituresData, expendituresSum = expenditureReview(user, begin, end)
    if not begin:
        begindate = datetime.datetime.today()
        begin = begindate.strftime('%Y-%m-%d')
    return render_template(
        "expreview.html",
        expendituresData=expendituresData,
        expendituresSum=expendituresSum,
        begin=begin,
        end=end)


@app.route("/increview", methods=["GET", "POST"])
@login_required
def increview():
    user = User.query.filter_by(id=session["user_id"]).first()
    begin = request.form.get("startdate")
    end = request.form.get("enddate")
    incomesData, incomesSum = incomesReview(user, begin, end)

    print(incomesData)

    if not begin:
        begindate = datetime.datetime.today()
        begin = begindate.strftime('%Y-%m-%d')
    return render_template(
        "increview.html",
        incomesData=incomesData,
        incomesSum=incomesSum,
        begin=begin,
        end=end)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        user = User.query.filter_by(email=request.form.get("email")).first()

        # Ensure username exists and password is correct
        if not user.id or not check_password_hash(str(user.hashstring), request.form.get("password")):
            return apology("invalid email and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = user.id

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# @app.route('/signup', methods=["GET", "POST"])
# def signup():
#     """
#     Register user
#     :return:
#     """
#     # param validation
#     if request.method == "POST":
#         if not request.form.get("email"):
#             return apology("must provide email", 400)
#         elif not request.form.get("password"):
#             return apology("must provide password", 400)
#         elif not request.form.get("confirmation"):
#             return apology("must provide confirmation", 400)
#         elif request.form.get("confirmation") != request.form.get("password"):
#             return apology("password and confirmation must match", 400)
#         else:
#             # generate hash for entered password
#             passwordHash = generate_password_hash(request.form.get("password"))


#             # check for user exists already

#             if User.query.filter_by(email=request.form.get("email")).count() > 0:
#                 return apology("User already exist", 403)

#             # add user to db
#             User.add_user(
#                 User,
#                 email=request.form.get("email"),
#                 hashstring=passwordHash)
#             # request base for id
#             id = User.query.filter_by(email=request.form.get("email")) \
#                 .first() \
#                 .id
#             # add id to session
#             session["user_id"] = id
#             return redirect("/")
#     else:
#         return render_template("signup.html")

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


@app.route("/expenditure_expand", methods=["GET"])
@login_required
def expenditure_expand():
    categoryName = request.args.get("category")
    begin = request.args.get("begin")
    end = request.args.get("end")
    user = User.query.filter_by(id=session["user_id"]).first()
    category = Category.query.filter_by(name=categoryName).first()
    expenditures = expandExpenditures(user, category, begin, end)
    print(categoryName)
    print(begin)
    print(end)

    return render_template(
        "expenditure_expand.html",
        expenditures=expenditures,
        category=categoryName)



@app.route("/downloadexp", methods=["GET"])
@login_required
def downloadExp():
    user = User.query.filter_by(id=session["user_id"]).first()
    expendituresList = getExpDumpList(user)

    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['date', 'category', 'name','price'])
    cw.writerows(expendituresList)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=expenditures.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@app.route("/downloadinc", methods=["GET"])
@login_required
def downloadInc():
    user = User.query.filter_by(id=session["user_id"]).first()
    incomeList = getIncDumpList(user)

    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['date', 'type', 'value'])
    cw.writerows(incomeList)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=incomes.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@app.route('/check_credentials', methods=["GET"])
def check_credentials():
    """
    Check user credentials
    :return:
    True or False
    """
    email = request.args.get("email")
    password = request.args.get("password")
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify(False)
    hashstring = str(user.hashstring)
    if check_password_hash(user.hashstring, password):
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
