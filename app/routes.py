from flask import request, render_template, flash, redirect
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import check_password_hash

from app.__init__ import app, db
from app.models import User, Notes, Contact, Url
from app.auth import signup_user, update_user
from app.src.script import (create_note, delete_note, create_contact, edit_contact, delete_contact, create_url,
                            delete_url)


# # # # # # # # # # # # # # # # Login # # # # # # # # # # # # # # # #

@app.route('/check', methods=['GET'])
def check_login():
    if current_user.is_authenticated:
        return redirect('/notes')
    else:
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', title='Entrar')
    else:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is not None:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect('/notes')
            else:
                flash('Incorrect user or password')
                return redirect('/login')
        else:
            flash('Usuario não existe')
            return redirect('/login')


@app.route('/signup', methods=['POST'])
def signup():
    query = signup_user(request)
    if query:
        return redirect('/notes')
    else:
        flash('Não foi possivel criar o usuario')
        return redirect('/login')


@app.route('/logout', methods=['GET'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect('/')
    else:
        return redirect('/login')


# # # # # # # # # # # # # # # # Profile # # # # # # # # # # # # # # # #

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'GET':
        return render_template('edit_user.html', user=current_user, title='Ajustes')
    else:
        query = update_user(request, current_user)
        print(query)
        if query is True:
            flash('Perfil atualizado')
            return redirect('/notes')
        else:
            flash(query)
            return redirect('/settings')


# # # # # # # # # # # # # # # # Notas # # # # # # # # # # # # # # # #

@app.route('/notes', methods=['GET'])
@login_required
def show_notes():
    notes = db.session.query(Notes).filter_by(user_id=current_user.id).all()
    return render_template('notes.html', user=current_user, notes=notes, title='Notas')


@app.route('/notes/add', methods=['GET', 'POST'])
@login_required
def add_new_note():
    if request.method == 'GET':
        return render_template('add_note.html', user=current_user, title='Notas')
    else:
        create_note(request, current_user)
        return redirect('/notes')


@app.route('/notes/del=<int:note_id>', methods=['GET'])
@login_required
def delete_note_by(note_id):
    delete_note(note_id)
    return redirect('/notes')


# # # # # # # # # # # # # # # # Contacts # # # # # # # # # # # # # # # #

@app.route('/contacts', methods=['GET'])
@login_required
def show_contacts():
    contacts = db.session.query(Contact).filter_by(user_id=current_user.id).all()
    return render_template('contacts.html', user=current_user, contacts=contacts, title='Contatos')


@app.route('/contacts/add', methods=['GET', 'POST'])
@login_required
def add_new_contact():
    if request.method == 'GET':
        return render_template('add_contact.html', user=current_user, title='Contatos')
    else:
        create_contact(request, current_user)
        return redirect('/contacts')


@app.route('/contacts/edit=<int:contact_id>', methods=['GET', 'POST'])
@login_required
def contact_edit(contact_id):
    contact = db.session.query(Contact).filter_by(id=contact_id, user_id=current_user.id).one()
    if request.method == 'GET':
        return render_template('edit_contact.html', user=current_user, contact=contact, title='Contatos')
    else:
        query = edit_contact(request, contact)
        if query:
            return redirect('/contacts')
        else:
            flash('O contato precisa de um nome')
            return redirect(f'/contacts/edit={contact.id}')


@app.route('/contacts/del=<int:contact_id>', methods=['GET'])
@login_required
def delete_contact_by(contact_id):
    delete_contact(contact_id)
    return redirect('/contacts')


# # # # # # # # # # # # # # # # Urls # # # # # # # # # # # # # # # #

@app.route('/urls', methods=['GET'])
@login_required
def show_urls():
    urls = db.session.query(Url).filter_by(user_id=current_user.id).all()
    return render_template('urls.html', user=current_user, urls=urls, title='Contatos')


@app.route('/urls/add', methods=['GET', 'POST'])
@login_required
def add_new_url():
    if request.method == 'GET':
        return render_template('add_url.html', user=current_user, title='Contatos')
    else:
        create_url(request, current_user)
        return redirect('/urls')


@app.route('/urls/del=<int:url_id>', methods=['GET'])
@login_required
def delete_url_by(url_id):
    delete_url(url_id)
    return redirect('/urls')


# # # # # # # # # # # # # # # # Gerais # # # # # # # # # # # # # # # #

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html', title='Inicio')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title='Sobre')


@app.errorhandler(405)
@app.errorhandler(404)
def not_found(e):
    if request.referrer:
        return redirect(request.referrer)
    else:
        return redirect('/home')
