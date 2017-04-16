from flask import render_template, request, url_for, redirect, abort
from sqlalchemy.ext.hybrid import hybrid_property
from slugify import slugify
from markdown2 import Markdown

from oxblog import app, db


markdowner = Markdown()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    slug = db.Column(db.String(500), unique=True)
    body = db.Column(db.Text, nullable=False)

    def __init__(self, title=None, body=None, slug=None, *args, **kwargs):
        self.title = title
        self.body = body
        if slug is None:
            self.slug = slugify(title)
        else:
            self.slug = slugify(slug)

    @property
    def html(self):
        return markdowner.convert(self.body)


@app.route('/', methods=['GET'])
def index():
    all_posts = Post.query.all()
    return render_template('index.html', posts=all_posts)


@app.route('/<slug>', methods=['GET'])
def post(slug):
    post = Post.query.filter_by(slug=slug).first()
    if post is None:
        return "No such post found.", 404
    if request.method == 'GET':
        return render_template('post.html', post=post)


@app.route('/<slug>/edit', methods=['GET', 'POST'])
def edit(slug):
    post = Post.query.filter_by(slug=slug).first()
    if post is None:
        abort(404)
    if request.method == 'GET':
        return render_template('new.html', post=post)
    post.title = request.form['title']
    post.body = request.form['body']
    db.session.commit()
    return url_for('post', post.slug)


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'GET':
        return render_template('new.html')
    post = Post(title=request.form['title'], body=request.form['body'])
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('post', slug=post.slug))