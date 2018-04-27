from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RU'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, body, owner):
        self.name = name
        self.body = body
        self.owner = owner
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'homepage', 'index', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/')
def homepage():
    return redirect('/blog')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect('/newpost')
        if not user:
            flash('Username does not exist')
            return redirect('/signup')
        if user.password != password:
            flash("Incorrect password")
            return render_template('login.html')
        else:
            flash("Try again")
            return render_template('/login')

 

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    del session['username']
    return redirect("/")

@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('signup.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if len(username) > 120 or len(username) < 3:
            flash("Username must be between 3 and 120 characters")
            return render_template('signup.html')
        if len(password) > 120 or len(password) < 3:
            flash("Password must be between 3 and 120 characters")
            return render_template('signup.html', username=username)
        if password != verify:
            flash("Passwords must match")
            return render_template('signup.html')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("User already exists")
            return render_template('signup.html')
        else:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = new_user.username
            flash("Welcome!")
            return redirect('/newpost')


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'GET':
        return render_template('newpost.html')

    if request.method == 'POST':
        blog_name = request.form['blog']
        body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()

        if len(blog_name) == 0:
            name_error = "Title is required"
        else:
            name_error = ""

        if len(body) == 0:
            body_error = "Content is required"
        else:
            body_error = ""

        if not name_error and not body_error:
            new_blog = Blog(blog_name, body, owner)
            db.session.add(new_blog)
            db.session.commit()
            blog_id = str(new_blog.id)
            return redirect('/individual?id=' + blog_id)

        else:
            return render_template('newpost.html', blog=blog_name, name_error=name_error, body=body, body_error=body_error)


@app.route('/blog')
def index():
    if request.args.get('id'):
        blog_id = request.args.get('id')
        blog = Blog.query.get(blog_id)
        return render_template('individual.html', blog=blog)
        
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)


@app.route('/individual')
def individual_blog():
    blog_id = request.args.get('id')
    blog = Blog.query.get(blog_id)
    return render_template('individual.html', blog=blog)



if __name__ == '__main__':
    app.run()