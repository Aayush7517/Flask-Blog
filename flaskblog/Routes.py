

from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user,logout_user

posts = [
    {
        'auther' : 'Aayush Chourasia',
        'title' : 'Blog no 1',
        'content' : 'First post content',
        'date_posted' : 'April 20, 2019'
    },

    {
        'auther' : 'Slok Chourasia',
        'title' : 'Blog no 2',
        'content' : 'Second post content',
        'date_posted' : 'April 27, 2022'
    }

]


@app.route('/')
def hello_world():
    return render_template('Home.html', posts = posts)

@app.route('/about')
def about():
    return render_template('about.html',title = 'About')

@app.route('/Register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('hello_world'))
    form = RegistrationForm()  
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.Password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to login', 'success')
        return redirect(url_for('Login'))
    return render_template('register.html', title = 'Register', form = form)


@app.route('/Login', methods = ['GET', 'POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('hello_world'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.Password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('hello_world'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form) 



@app.route('/Logout')
def Logout():
    logout_user()
    return redirect(url_for('Login'))



@app.route('/account')
def account():
    return render_template('account.html', title='account')



























