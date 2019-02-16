from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    hashstring = db.Column(db.String, nullable=False)

    def add_user(self, email, hashstring):
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
    value = db.Column(db.Integer, nullable=False)

    def add_income(self, user, date, type, value):
        income = Income(user_id=user.id, date=date, type=type, value=value)
        db.session.add(income)
        db.session.commit()


class Expenditure(db.Model):
    __tablename__ = "expenditures"
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    categories_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def add_expenditure(self, user, category, date, name, price):
        expenditure = Expenditure(user_id=user.id, categories_id=category.id, date=date, name=name, price=price)
        db.session.add(expenditure)
        db.session.commit()

    def del_expenditure(self, expenditure_id):
        expenditure = Expenditure.query.filter_by(id=expenditure_id).first()
        db.session.delete(expenditure)
        db.session.commit()
