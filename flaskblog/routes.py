import os
import secrets
from flask import render_template, url_for, redirect, flash, request, abort
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, ResetPasswordForm, RequestResetForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route("/") 
@app.route("/home")
def home():
	page = request.args.get('page', 1, type=int) 
	posts = Post.query.order_by(Post.user_id).paginate(page=page, per_page = 2) # order by title in desc order
	return render_template('home.html',posts=posts, title = 'Home')

@app.route("/about")
def about():
	return render_template('about.html' , title = 'About')

@app.route("/register" ,methods= ['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username = form.username.data, email = form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Your account has been created! You are now able to log in ','success')
		return redirect(url_for('login'))
	return render_template('register.html', title = 'Register' , form = form)


@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember = form.remember.data)
			next_page = request.args.get('next')
			if next_page:
				return redirect(url_for('account'))
			else:
				flash(f"Login Successfull !!",'success')
				return redirect(url_for('home'))
		else:
			flash(f"Login failed Username or Password incorrect",'danger')
	return render_template('login.html', title = 'Login', form = form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash(f"Your account has been updated", 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email

	image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
	return render_template('account.html', title = 'Account', image_file = image_file, form = form)




@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title = form.title.data, content = form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash("Post has been added",'success')
		return redirect(url_for('home'))
	return render_template('create_post.html', title = 'New Post', form=form ,legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html',title =post.title, post=post )

@app.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash("Post has been updated" ,'success')
		return redirect(url_for('post', post_id = post.id))
	elif request.method =='GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title='Update Post',form = form, legend= 'Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash("Post has been deleted!", 'success')
	return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(author=user).paginate(page=page, per_page=2)
	return render_template('user_posts.html', posts=posts, user=user)


def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request',
				  sender='noreply@demo.com',
				  recipients=[user.email])
	msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If not made by you, ignore 
	'''
	mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		flash("Logout before changing the password",'danger')
		return redirect(url_for('home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash("An email has been sent for password reset",'info')
		return redirect(url_for('login'))
	return render_template('reset_request.html',title='Reset Request', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		flash("Logout before changing the password",'danger')
		return redirect(url_for('home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash("This is an invalid token",'warning')
		return redirect(url_for('reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash(f'Your password has been updated!!','success')
		return redirect(url_for('login'))
	return render_template('reset_token.html', title="Reset Password", form=form)
