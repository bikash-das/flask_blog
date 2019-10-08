from flask import render_template, url_for,flash,redirect, request
from flaskblog.forms import RegistrationForm, LoginForm
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
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    #create new template
    return render_template('account.html', title='Account')
