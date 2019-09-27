from flask import Flask,render_template, url_for,flash,redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

# set secret key
app.config['SECRET_KEY'] = 'd6ad308f0cf0e8542f894171ea38fb31'

#let's suppose we got this data from database, a dictionary
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



if __name__ == '__main__':
    app.run(debug=True)