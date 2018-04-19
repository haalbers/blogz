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

    def __init__(self, name, body):
        self.name = name
        self.body = body
    


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

        if len(blog_name) == 0:
            name_error = "Title is required"
        else:
            name_error = ""

        if len(body) == 0:
            body_error = "Content is required"
        else:
            body_error = ""

        if not name_error and not body_error:
            new_blog = Blog(blog_name, body)
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