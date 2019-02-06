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

    def flush_session(self):
        db.session.flush()
