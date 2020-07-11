import os
import secrets
from PIL import Image
from flask import render_template, redirect, request, url_for, flash, abort
from flaskblog.models import User
from flaskblog.forms import SignUp, SignIn, UpdateProfile
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

cities = db.session.query(User.city).distinct()

@app.route('/')
def index():
	return render_template('index.html', cities = cities)

@app.route('/about', methods = ['GET', 'POST'])
def about():
	return render_template('about.html', title = 'about')

@app.route('/test')
def test():
	return render_template('test.html', cities = cities)

@app.route('/home')
def home():
	return redirect('/')

# @app.route('/faq') 
# def faq():
# 	questions = {
# 					"1. Does my religion support eye donation?": "All major religions openly support eye donation and encourage their followers to consider “paying it forward” by giving the gift of sight also they view it as final act of love and generosity.",
# 					"2. Is there a cost to be an eye donor?": "Eye donation is entirely voluntary. Selling or buying human eyes or any other organs is illegal and is a punishable offense under the Transplantation of Human Organs Act (THOA, 1994).  In fact, any cost involved with cornea retrieval is borne by the eye bank.",
# 					"3. Does donation affect funeral plans?": "DONATION IS REGARDED AS A GIFT AND THERE ARE NO CHARGES TO THE DONOR FAMILY.",
# 					"4. Does registering as a donor change my patient care?": "Funeral arrangements of your choice are possible, including a viewing. Through the entire donation process the body is treated with care and respect. Following donation, funeral arrangements can continue as planned",
# 					"5. Does my social and/or financial status play any part in whether or not any visually impaired one will receive donated eye?": "DONATED HUMAN EYES ARE NECESSARY FOR THE PRESERVATION AND RESTORATION OF SIGHT. MORE THAN 92% OF MANITOBANS RECEIVING A CORNEAL TRANSPLANT EACH YEAR HAD THEIR VISION SUCCESSFULLY RESTORED.",
# 					"6. Why is it important for people of every community to donate?": "Why is it important for people of every community to donate?Although donation and transplantation can take place successfully between individuals from different racial or ethnic groups."
# 	}
# 	return render_template('faq.html', questions = questions)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = SignUp()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username = form.username.data, accountName = form.accountName.data, city = form.city.data, email = form.email.data, password = hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created, now you can Signin', 'success')
		return redirect(url_for('signin'))
	return render_template('signup.html', title = 'Sign Up', form = form)

@app.route('/signin', methods = ['GET', 'POST'])
def signin():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = SignIn()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember = form.remember_me.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Invalid Credentials', 'danger')
	return render_template('signin.html', title = 'Sign In', form = form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn


@app.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
	form = UpdateProfile()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.avatar = picture_file
		current_user.username = form.username.data
		form.accountName.data = current_user.accountName
		form.city.data = current_user.city
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.accountName.data = current_user.accountName
		form.city.data = current_user.city
		form.email.data = current_user.email
	image_file = url_for('static', filename = 'profile_pics/' + current_user.avatar)
	return render_template('account.html', title = 'profile', image_file = image_file, form = form)

@app.route('/<city>')
def pressedCity(city):
	listed_users = User.query.filter_by(city = city)
	return render_template('city.html', title = city, users = listed_users)

# @app.route('/user/<name>')
# @login_required
# def user_profile():
# 	form.accountName.data = current_user.accountName
# 	form.city.data = current_user.city
# 	form.email.data = current_user.email
# 	image_file = url_for('static', filename = 'profile_pics/' + current_user.avatar)
# 	return render_template('user_profile.html', title = current_user.username, image_file = image_file)
