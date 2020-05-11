from flask import (render_template,request,session,
                   url_for,redirect,g,abort)
from flask_login import LoginManager , login_user, logout_user, login_required,current_user
from werkzeug.security import check_password_hash
from peewee import DoesNotExist
from app import app
import models 
import forms

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.Users.get(models.Users.id == userid)
    except DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response




@app.route('/')
def index():
    return render_template('index.html',file_name="index")


@app.route('/register',methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print("Yay, you registered!", "success")
            try:
                models.Users.create_user(
                            email=form.email.data,
                            password=form.password.data)
                return redirect(url_for('register_confirm'))
            except ValueError:
                print("user is exist")
            else:
                #TODO return error to templates if user is exisit
                return render_template('register.html',form=form)
           
    return render_template('register.html',form=form)
    
@app.route('/register_confirm')
def register_confirm():
    return render_template('register_confirm.html')


@app.route('/login',methods=['POST','GET'])

def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
               user = models.Users.get(models.Users.email == form.email.data)
            except DoesNotExist:
                print("Your email or password doesn't match!", "error")
            else:
                if check_password_hash(user.password, form.password.data):
                    login_user(user)
                    print("You've been logged in!", "success")
                    next = request.args.get('next')
                    return redirect(next or url_for('index'))
                else:
                    print("Your email or password doesn't match!", "error")

    return render_template('login.html',form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')



@app.route("/settings")
@login_required
def settings():
    pass

