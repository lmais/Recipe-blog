from flask import render_template, url_for, flash, redirect, request, abort
from recipeblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, SearchForm
from recipeblog.models import User, Post, Favorite
from recipeblog import app, db, bcrypt, logging
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image
from sqlalchemy import desc

@ app.route("/", methods=['GET', 'POST'])
@ app.route("/home", methods=['GET', 'POST'])
def home():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('home.html', posts=posts)


@ app.route("/about")
def about():
    return render_template('about.html', title='About')


@ app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@ app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful, please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

def save_recipe_picture(recipe_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(recipe_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/recipe_pics', picture_fn)
    output_size = (400, 400) ######################################(125,125)###########################################################
    i = Image.open(recipe_picture)
    #i.thumbnail(output_size)#################################################################################################
    i.save(picture_path)
    return picture_fn

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post_image = 'default_image.jpg'
        if form.recipe_picture.data:
            picture_file = save_recipe_picture(form.recipe_picture.data)
            post_image = picture_file
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user, image=post_image)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
     
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit(): 
        picture_file = save_recipe_picture(form.recipe_picture.data)
        post.image = picture_file
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('post', post_id = post.id))
    elif request.method == 'GET':   
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/post/<int:post_id>/favorite", methods=['GET','POST'])
@login_required
def favorite_post(post_id):
    f = Favorite(post_id=post_id, user_id=current_user.id)
    db.session.add(f)
    db.session.commit()
    flash('This post has been added to your favorites list!', 'success')
    return redirect(url_for('home'))

@ app.route("/favorites", methods=['GET'])
@login_required
def favorites():   
    user_favorites = db.session.query(Favorite).filter(Favorite.user_id == current_user.id).all()
    fav_post_ids = []
    for f in user_favorites:
        fav_post_ids.append(f.post_id)
    fav_posts = db.session.query(Post).filter(Post.id.in_(fav_post_ids)).order_by(Post.id.desc())
  
    return render_template('favorites.html', posts=fav_posts)



def search():
    form = SearchForm()
    if form.search.data:
        search_text = form.search.data
        search = db.session.query(Posts).filter(Post.content.contains(search_text)).all()
        search_ids = []
        for s in search:
            search_ids.append(s.post_id)
        search_posts = db.session.query(Post).filter(Post.id.in_(fav_post_ids)).order_by(Post.id.desc())
    
        return render_template('search_results.html', posts=search_posts) 


    
