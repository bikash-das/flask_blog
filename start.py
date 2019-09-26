from flask import Flask,render_template, url_for
app = Flask(__name__)

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




if __name__ == '__main__':
    app.run(debug=True)