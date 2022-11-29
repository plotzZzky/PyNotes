from app import db, User
from werkzeug.security import generate_password_hash
from flask_login import login_user


def create_username(username):
    if len(username) > 3:
        return username
    else:
        return None


def create_password(password, password_b, min_password):
    if password == password_b and len(password) >= min_password:
        return password
    else:
        return None


def create_email(email):
    if '@' in email and len(email) > 11:
        return email
    else:
        return None


def update_username(user, username):
    user.username = username
    db.session.commit()


def update_email(user, email):
    if '@' in email and len(email) >= 10:
        user.email = email
        db.session.commit()


def update_password(user, password):
    if len(password) >= 3:
        user.password = generate_password_hash(password)
        db.session.commit()


def update_profile_picture(pic, user_id):
    user = User.query.filter_by(id=user_id).first()
    user.profile_pic = pic
    db.session.commit()


def update_user(request, current_user):
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    pwd = request.form['pwd']
    user_id = current_user.id
    current_username = current_user.username
    user = db.session.query(User).filter_by(id=user_id).first()
    if username != current_username and username != '' and len(username) >= 3:
        update_username(user, username)
    if email != current_user.email:
        update_email(user, email)
    if password == pwd and len(password) >= 3:
        if generate_password_hash(password) != current_user.password:
            update_password(user, password)


def signup_user(request):
    f_name = request.form['username']
    f_email = request.form['email']
    pwd = request.form['password']
    pwssd = request.form['pwd']
    username = create_username(f_name)
    email = create_email(f_email)
    passwd = create_password(pwd, pwssd, 3)
    if username and email and passwd is not None:
        password = generate_password_hash(passwd)
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return True
    else:
        return False
