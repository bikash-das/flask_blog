import secrets
import os
from PIL import Image
from flask import render_template, url_for,flash,redirect, request
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog import app # becoz decorators uses app (@app)
from flaskblog import db,bcrypt # db , dcrypt in init file
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {
        'author':'Bikash Das',
        'title':'Blog Post',
        'content': 'First post content',
        'date_posted':'September 25, 2019'
    },
    {
        'author':'Mahesh Das',
        'title':'Blog Post', 
        'content': 'Second post content',
        'date_posted':'September 25, 2019'
    },
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html",title="bikash")

@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():   #ffor one time message, success message
        # lesson 6
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) #new instance of user info that they passed in the fields
        db.session.add(user) #add the current user
        db.session.commit() # make changes to the database
        # lesson 6  #####
        flash('Your account has been created! You are now able to log in', 'success')
        # redirect after success, to home page, import redirect
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm() 
    if form.validate_on_submit():
        # lesson 6
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            #user exist and password is valid 
            # logthem in using flask extension
            login_user(user,remember=form.remember.data) # remember is true or false
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home'))

        # ########### lesson 6
        else:       
            flash('Login Unsuccessful. Please check email and password','danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    # it already know what user is logged in
    logout_user() #simply call this and current_user is logged out, simple
    return redirect(url_for('home'))

def save_picture(form_picture):
    # name collision can occur, we will change the name of the file using secret module
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # resize the image to save it
    output_size = (250,250)
    i = Image.open(form_picture)
    i.thumbnail(output_size,Image.LANCZOS)

    i.save(picture_path)
    
    return picture_fn #return to user so that it can be set in profile pic





@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            # set user profile picture
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file #image_file is in model varaible
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated','success')
        return redirect(url_for('account')) #redirect or i@app.route("/act falls into another post request,
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file,form=form)
