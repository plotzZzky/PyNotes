from app.__init__ import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String())
    email = db.Column(db.String(128), unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String())
    text = db.Column(db.String())
    date = db.Column(db.Date())
    color = db.Column(db.String())

    def __init__(self, title, text, date, color, user_id):
        self.user_id = user_id
        self.title = title
        self.text = text
        self.date = date
        self.color = color


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String())
    lastname = db.Column(db.String())
    telephone = db.Column(db.String())
    email = db.Column(db.String())
    social = db.Column(db.String())


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    site_name = db.Column(db.String())
    url = db.Column(db.String())
