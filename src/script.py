from app import db, Notes, Contact, Url
from datetime import datetime


def create_note(request, user):
    title = request.form['title']
    text = request.form['text']
    date = datetime.today().strftime('%d/%m/%Y')
    color = request.form['color']
    user_id = user.id
    note = Notes(user_id=user_id, title=title, text=text, date=date, color=color)
    db.session.add(note)
    db.session.commit()
    return True


def delete_note(note_id):
    note = db.session.query(Notes).filter_by(id=note_id).one()
    db.session.delete(note)
    db.session.commit()


def create_contact(request, user):
    name = request.form['name'].capitalize()
    lastname = request.form['lastname'].capitalize()
    telephone = request.form['telephone']
    email = request.form['email']
    social = request.form['social']
    user_id = user.id
    contact = Contact(user_id=user_id, name=name, lastname=lastname, telephone=telephone, email=email, social=social)
    db.session.add(contact)
    db.session.commit()
    return True


def edit_contact(request, contact):
    if request.form['name'] != ' ':
        contact.name = request.form['name'].capitalize()
    else:
        return False
    contact.lastname = request.form['lastname'].capitalize()
    contact.telephone = request.form['telephone']
    contact.email = request.form['email']
    contact.social = request.form['social']
    db.session.commit()
    return True


def delete_contact(contact_id):
    contact = db.session.query(Contact).filter_by(id=contact_id).one()
    db.session.delete(contact)
    db.session.commit()


def create_url(request, user):
    site_name = request.form['title']
    url = request.form['url']
    user_id = user.id
    url = Url(user_id=user_id, site_name=site_name, url=url)
    db.session.add(url)
    db.session.commit()


def delete_url(url_id):
    url = db.session.query(Url).filter_by(id=url_id).one()
    db.session.delete(url)
    db.session.commit()
