from app.__init__ import db
from app.models import User

from werkzeug.security import generate_password_hash
from flask_login import login_user


def create_username(request):
    username = request.form['username']
    if len(username) > 3:
        return username
    else:
        return None


def create_password(request, min_password):
    password = request.form['password']
    pwd = request.form['pwd']
    if password == pwd and len(password) > min_password:
        result = generate_password_hash(password)
        return result
    else:
        return None


def create_email(request):
    email = request.form['email']
    if '@' in email and len(email) > 11:
        return email
    else:
        return None


def update_username(user, request):
    new_username = request.form['username']
    if new_username != user.username and new_username != '':
        if len(new_username) > 3:
            user.username = new_username
            db.session.commit()
            return True
        else:
            return 'O username de ter no minimo 3 caracteres'
    return True


def update_email(user, request):
    email = request.form['email']
    if email != user.email:
        if '@' in email and len(email) >= 10:
            user.email = email
            db.session.commit()
            return True
        else:
            return 'Email invalido'
    return True


def update_password(user, request):
    password = request.form['password']
    pwd = request.form['pwd']
    if password != '' and pwd != '':
        if password == pwd:
            if len(password) >= 3:
                user.password = generate_password_hash(password)
                db.session.commit()
                return True
            else:
                return 'A Senha precisa ter no minimo 3 caracteres'
        else:
            return 'As senhas precisam ser iguais'
    return True


def update_user(request, current_user):
    user = db.session.query(User).filter_by(id=current_user.id).first()
    username = update_username(user, request)
    if username is not True:
        return username
    email = update_email(user, request)
    if email is not True:
        return email
    password = update_password(user, request)
    if password is not True:
        return password
    else:
        return True


def signup_user(request):
    username = create_username(request)
    email = create_email(request)
    password = create_password(request, 3)
    if username and email and password is not None:
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return True
    else:
        return False
