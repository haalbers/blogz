from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, name):
        self.name = name
    


@app.route('/')
def homepage():
    return redirect('/blog')

@app.route('/newpost', methods=['GET'])
def new_post():
    return render_template('newpost.html')


@app.route('/newpost', methods=['POST'])
def newpost():
        blog_name = request.form['blog']
        body = request.form['body']
        new_blog = Blog(blog_name)
        db.session.add(new_blog)
        db.session.commit()

        return render_template('blog.html', name=name, body=body)


@app.route('/blog')
def index():
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)


if __name__ == '__main__':
    app.run()