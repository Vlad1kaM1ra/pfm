from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    hashstring = db.Column(db.String, nullable=False)

    @staticmethod
    def add_user(email, hashstring):
        user = User(email=email, hashstring=hashstring)
        db.session.add(user)
        db.session.commit()


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False, unique=True)


class Income(db.Model):
    __tablename__ = "income"
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String, nullable=False)
    value = db.Column(db.Numeric(10, 2), nullable=False)

    @staticmethod
    def add_income(user, date, type, value):
        income = Income(user_id=user.id, date=date, type=type, value=value)
        db.session.add(income)
        db.session.commit()

    @staticmethod
    def del_income(income_id):
        income = Income.query.filter_by(id=income_id).first()
        db.session.delete(income)
        db.session.commit()


class Expenditure(db.Model):
    __tablename__ = "expenditures"
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    categories_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    @staticmethod
    def add_expenditure(user, category, date, name, price):
        expenditure = Expenditure(user_id=user.id, categories_id=category.id, date=date, name=name, price=price)
        db.session.add(expenditure)
        db.session.commit()

    @staticmethod
    def del_expenditure(expenditure_id):
        expenditure = Expenditure.query.filter_by(id=expenditure_id).first()
        db.session.delete(expenditure)
        db.session.commit()


def get_expenditure_dump_list(user):
    res = db.session.query(Expenditure.date, Category.name, Expenditure.name, Expenditure.price) \
        .outerjoin(Category, Category.id == Expenditure.categories_id) \
        .filter(Expenditure.user_id == user.id) \
        .order_by(Expenditure.date) \
        .all()
    return res


def get_income_dump_list(user):
    res = db.session.query(Income.date, Income.type, Income.value) \
        .filter(Income.user_id == user.id) \
        .order_by(Income.date) \
        .all()
    return res
