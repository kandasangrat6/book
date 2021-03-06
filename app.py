from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import request
from database import app, db, Users
from sqlalchemy.exc import IntegrityError

db.create_all()

bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired()])



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        flash("Invalid Credential, Try again")
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    login_form = LoginForm()
    if form.validate_on_submit():
        if form.password.data == form.confirm_password.data:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash("User  {} has been created!".format(str(form.username.data)))

                return render_template('login.html', form= login_form)
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
            except IntegrityError as error:
                flash("User already exists. Please login instead")
        error = "Error"

    return render_template('signup.html', form= form, flash=flash)


@app.route('/dashboard')
@login_required
def dashboard():
    
    return render_template('dashboard.html', name="erfan", data = "Book1")


@app.route("/export")
def export():
    #data = zip(Book_titles,Book_prices)
    return render_template("export_books.html", data = ("book","idk"))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route("/testform", methods=['GET','POST'])
def form():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash("Your username or password doesn't match")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!")
                return redirect(url_for('index'))
            else:
                flash("Your username or password doesn't match")
    return render_template("test_forms.html")


if __name__ == '__main__':
    app.run(debug=True, host="10.254.25.210")
