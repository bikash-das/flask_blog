from flask import render_template, url_for,flash,redirect
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog import app # becoz decorators uses app (@app)
from flaskblog.models import User, Post



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
    form = RegistrationForm()
    if form.validate_on_submit():   #for one time message, success message
        flash(f'Account created for {form.username.data}!', 'success')
        # redirect after success, to home page, import redirect
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm() 
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password','danger')
    return render_template('login.html', title='Login', form=form)

