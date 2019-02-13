from flask import redirect, render_template, request, session
from functools import wraps
import datetime
from models import *


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def getDateDiapazon():
    # get date period
    begindate = datetime.datetime.today()
    begindate = begindate.replace(day=1)
    begin = begindate.strftime('%Y-%m-%d')

    try:
        nextmonthdate = begindate.replace(month=begindate.month + 1)
    except ValueError:
        if begindate.month == 12:
            nextmonthdate = begindate.replace(year=begindate.year + 1, month=1)

    end = nextmonthdate.strftime('%Y-%m-%d')

    print(begin)
    print(end)
    return [begin, end]


def currentMonthExpenditureSummary(user):
    begin, end = getDateDiapazon()
    # generates expenditures category, sum tuple
    expendituresData = []
    expendituresSum = 0
    categories = Category.query.all()
    overalSum = 0
    for category in categories:
        categorySum = 0
        expenditures = Expenditure \
            .query \
            .filter_by(user_id=user.id) \
            .filter_by(categories_id=category.id) \
            .filter(Expenditure.date >= begin) \
            .filter(Expenditure.date < end) \
            .all()
        for expenditure in expenditures:
            categorySum += expenditure.price
        expendituresData.append((category.name, categorySum))
        # accumulates overal sum from all categories
        expendituresSum += categorySum
    return [expendituresData, expendituresSum]


def currentMonthIncomeSummary(user):
    begin, end = getDateDiapazon()
    # get income data for period
    incomes = Income \
        .query \
        .filter_by(user_id=user.id) \
        .filter(Income.date >= begin) \
        .filter(Income.date < end) \
        .all()

    incomesTotal = 0
    for income in incomes:
        incomesTotal += income.value

    return [incomes, incomesTotal]
