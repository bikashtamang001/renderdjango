from . import db
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from .models import Post,User
from flask_paginate import Pagination

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()

    post = Post.query.order_by(Post.id.desc())

    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    pages = post.paginate(page = page, per_page = 2)
    return render_template("home.html", user = current_user, posts = post, pages= pages)


@views.route("/create-post", methods = ['GET','POST'])
#login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty ', category = 'error')
        else:
            post = Post(text=text, author = current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))
    return render_template('create_post.html',user = current_user)

@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id = id).first()

    if not post:
        flash("Post doesnot exist.", category='error')
    # elif current_user.id != post.id:
    #     flash("You are not allowed to delete the post.")
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')
    
    return redirect(url_for('views.home'))

@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username = username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))
    
    post = Post.query.filter_by(author = user.id).order_by(Post.date_created.desc())
    
    
    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    pages = post.paginate(page = page, per_page = 2)

    return render_template("posts.html", user = current_user, posts = post, username = username,pages =pages)


