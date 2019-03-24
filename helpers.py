from flask import redirect, render_template, session
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


def get_date_diapazon():
    """
    Generate date range for current month
    :return:
    first and last date of current month
    """
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


def current_month_expenditure_summary(user):
    """
    Get info about expenditures in current month
    :param user:
    :return:
    Summary data by categories
    and expenditures sum
    """
    begin, end = get_date_diapazon()
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


def expenditure_review_data(user, begin, end):
    """
    Generate reports for
    today
    specified day
    time period
    :param user:
    :param begin:
    :param end:
    :return:
    sum by categories for period
    and overall sum
    """
    categories = Category.query.all()
    expendituresData = []
    expendituresSum = 0
    if not begin and not end:
        begindate = datetime.datetime.today()
        begin = begindate.strftime('%Y-%m-%d')
        for category in categories:
            categorySum = 0
            expenditures = Expenditure \
                .query \
                .filter_by(user_id=user.id) \
                .filter_by(categories_id=category.id) \
                .filter_by(date=begin) \
                .all()
            for expenditure in expenditures:
                categorySum += expenditure.price
            expendituresData.append((category.name, categorySum))
            # accumulates overal sum from all categories
            expendituresSum += categorySum
        return [expendituresData, expendituresSum]
    elif not end:
        date = datetime.datetime.strptime(begin, '%Y-%m-%d').date()
        for category in categories:
            categorySum = 0
            expenditures = Expenditure \
                .query \
                .filter_by(user_id=user.id) \
                .filter_by(categories_id=category.id) \
                .filter_by(date=date) \
                .all()
            for expenditure in expenditures:
                categorySum += expenditure.price
            expendituresData.append((category.name, categorySum))
            # accumulates overal sum from all categories
            expendituresSum += categorySum
        return [expendituresData, expendituresSum]
    else:
        begin = datetime.datetime.strptime(begin, '%Y-%m-%d').date()
        end = datetime.datetime.strptime(end, '%Y-%m-%d').date()
        for category in categories:
            categorySum = 0
            expenditures = Expenditure \
                .query \
                .filter_by(user_id=user.id) \
                .filter_by(categories_id=category.id) \
                .filter(Expenditure.date >= begin) \
                .filter(Expenditure.date <= end) \
                .all()
            for expenditure in expenditures:
                categorySum += expenditure.price
            expendituresData.append((category.name, categorySum))
            # accumulates overal sum from all categories
            expendituresSum += categorySum
        return [expendituresData, expendituresSum]


def incomes_review_data(user, begin, end):
    """
    Generate reports for
    today
    specified day
    time period
    :param user:
    :param begin:
    :param end:
    :return:
    incomes for period
    and overall sum
    """
    incomesSum = 0
    if not begin and not end:
        begindate = datetime.datetime.today()
        begin = begindate.strftime('%Y-%m-%d')

        incomesData = Income \
            .query \
            .filter_by(user_id=user.id) \
            .filter_by(date=begin) \
            .order_by(Income.date) \
            .all()
    elif not end:
        date = datetime.datetime.strptime(begin, '%Y-%m-%d').date()
        incomesData = Income \
            .query \
            .filter_by(user_id=user.id) \
            .filter_by(date=date) \
            .order_by(Income.date) \
            .all()
    else:
        begin = datetime.datetime.strptime(begin, '%Y-%m-%d').date()
        end = datetime.datetime.strptime(end, '%Y-%m-%d').date()
        incomesData = Income \
            .query \
            .filter_by(user_id=user.id) \
            .filter(Income.date >= begin) \
            .filter(Income.date <= end) \
            .order_by(Income.date) \
            .all()
    for income in incomesData:
        incomesSum += income.value

    return [incomesData, incomesSum]


def expenditure_summary(user, date, category):
    """
    Generate date for expenditures for specified
    category in specified date range
    :param user:
    :param date:
    :param category:
    :return:
    Date by items
    overall sum
    """
    expenditureData = []
    expenditures = Expenditure \
        .query \
        .filter_by(user_id=user.id) \
        .filter_by(categories_id=category.id) \
        .filter_by(date=date) \
        .all()
    expenditureSum = 0
    for expenditure in expenditures:
        expenditureData.append((expenditure.name, expenditure.price, expenditure.id))
        expenditureSum += expenditure.price
    return [expenditureData, expenditureSum]


def current_month_income_summary(user):
    """
    Sumary of incomes
    :param user:
    :return:
    Incomes item by item
    overall sum
    """
    begin, end = get_date_diapazon()
    # get income data for period
    incomes = Income \
        .query \
        .filter_by(user_id=user.id) \
        .filter(Income.date >= begin) \
        .filter(Income.date < end) \
        .order_by(Income.date) \
        .all()

    incomesTotal = 0
    for income in incomes:
        incomesTotal += income.value

    return [incomes, incomesTotal]


def expand_expenditures(user, category, begin, end):
    """
    Expendetures details for specified category
    in specified time period
    Data for ajax request
    :param user:
    :param category:
    :param begin:
    :param end:
    :return:
    Expenditures item by item
    """
    if not end or end == "None":
        begin = datetime.datetime.strptime(begin, '%Y-%m-%d').date()
        expenditures = Expenditure \
            .query \
            .filter_by(user_id=user.id) \
            .filter_by(categories_id=category.id) \
            .filter_by(date=begin) \
            .order_by(Expenditure.date) \
            .all()
        return expenditures
    else:
        begin = datetime.datetime.strptime(begin, '%Y-%m-%d').date()
        end = datetime.datetime.strptime(end, '%Y-%m-%d').date()
        expenditures = Expenditure \
            .query \
            .filter_by(user_id=user.id) \
            .filter_by(categories_id=category.id) \
            .filter(Expenditure.date >= begin) \
            .filter(Expenditure.date <= end) \
            .order_by(Expenditure.date) \
            .all()
        return expenditures
