# coding: utf-8
from __future__ import unicode_literals
from dircache import listdir

from flask import Flask, render_template, redirect, url_for, request, flash, \
    make_response
from flask_login import\
    LoginManager,\
    current_user,\
    login_user,\
    logout_user,\
    login_required
from flask import send_from_directory
from os import path

from sqlalchemy.orm import joinedload
from werkzeug.exceptions import abort

from database import db_session, init_db
from forms import LoginForm, RegisterForm, MessageForm
from models import User, UserDoesntExist, UserExists, Message

app = Flask(__name__)

app.config['DEBUG'] = False
# app.config['SECRET_KEY'] = '??????????'   # Set it right

# ORIGIN = 'http://localhost:5000'  # Set it right

init_db()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Musisz się najpierw zalogować."
login_manager.login_message_category = 'info'


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@login_manager.user_loader
def load_user(user_id):
    return User.load(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        try:
            user = User.login(form.username.data, form.password.data)
            login_user(user)
            return redirect(request.args.get('next') or url_for('index'))
        except UserDoesntExist:
            flash("Logowanie nieudane.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        try:
            User.register(
                form.username.data,
                form.password.data,
                form.public_key.data
            )
            flash("Konto założone! Możesz się teraz zalogować.", 'success')

            return redirect(url_for('login'))
        except UserExists:
            flash("Konto o tej nazwie użytkownika już istnieje.", 'danger')

    return render_template('register.html', form=form)


@app.route('/list_users')
@login_required
def list_users():
    users = User.query.filter(User.username != current_user.username).all()
    return render_template('list_users.html', users=users)


@app.route('/list_messages')
@login_required
def list_messages():
    messages = Message.query.options(joinedload('sender'))\
        .filter(Message.recipient_id == current_user.id).all()
    return render_template('list_messages.html', messages=messages)


@app.route('/send_message/<username>', methods=['GET', 'POST'])
@login_required
def send_message(username):
    form = MessageForm(request.form)
    if request.method == 'POST' and form.validate():
        Message.register(
            form.encmessage.data,
            form.subject.data,
            form.recipient.data,
            current_user.id
        )
        flash("Wiadomość wysłana!", 'success')
        return redirect(url_for('index'))

    user = User.query.filter(User.username == username).first()
    if not user or user.username == current_user.username:
        flash("Użytkownik nie istnieje lub jest niepoprawny.", 'danger')
        return redirect(url_for('index'))
    return render_template('send_message.html', recipient=user, form=form)


@app.route('/read_message/<message_id>')
@login_required
def read_message(message_id):
    if request.headers.get('referer') != (ORIGIN + '/list_messages'):
        abort(make_response("CSRF attack detected", 403))
    message = Message.query.options(joinedload('sender'))\
        .filter(Message.id == message_id).first()
    if not message or message.recipient_id != current_user.id:
        abort(404)
    return render_template('read_message.html', message=message)
