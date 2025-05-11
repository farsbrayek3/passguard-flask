from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from cryptography.fernet import Fernet
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Fernet key management
def load_key():
    key_path = os.path.join(BASE_DIR, 'secret.key')
    if not os.path.exists(key_path):
        key = Fernet.generate_key()
        with open(key_path, 'wb') as key_file:
            key_file.write(key)
    else:
        with open(key_path, 'rb') as key_file:
            key = key_file.read()
    return key

key = load_key()
fernet = Fernet(key)

# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

class PasswordEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    site = db.Column(db.String(150), nullable=False)
    login = db.Column(db.String(150), nullable=False)
    encrypted_password = db.Column(db.LargeBinary, nullable=False)
    note = db.Column(db.Text)
    link = db.Column(db.String(300))
    user = db.relationship('User', backref=db.backref('password_entries', lazy=True))

# Forms
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=150)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError('Username already exists. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=150)])
    submit = SubmitField('Login')

class PasswordEntryForm(FlaskForm):
    site = StringField('Site', validators=[InputRequired()])
    login = StringField('Login (email/username)', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    note = StringField('Note')
    link = StringField('Link')
    submit = SubmitField('Save')

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# ROUTES

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    entries = PasswordEntry.query.filter_by(user_id=current_user.id).all()
    for entry in entries:
        entry.decrypted_password = fernet.decrypt(entry.encrypted_password).decode()
    return render_template('dashboard.html', username=current_user.username, entries=entries)

@app.route('/add_password', methods=['GET', 'POST'])
@login_required
def add_password():
    form = PasswordEntryForm()
    if form.validate_on_submit():
        encrypted_password = fernet.encrypt(form.password.data.encode())
        entry = PasswordEntry(
            user_id=current_user.id,
            site=form.site.data,
            login=form.login.data,
            encrypted_password=encrypted_password,
            note=form.note.data,
            link=form.link.data
        )
        db.session.add(entry)
        db.session.commit()
        flash('Password entry saved!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_password.html', form=form)

if __name__ == '__main__':
    if not os.path.exists(os.path.join(BASE_DIR, 'instance', 'users.db')):
        os.makedirs(os.path.join(BASE_DIR, 'instance'), exist_ok=True)
        with app.app_context():
            db.create_all()
    app.run(debug=True)