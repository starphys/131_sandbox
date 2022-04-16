from app import myapp_obj, db, basedir
from app.forms import LoginForm, SignUpForm
from app.models import User
from flask import redirect, render_template, flash, request, url_for
from flask_login import current_user, login_user, logout_user, login_required

import os
from werkzeug.utils import secure_filename


@myapp_obj.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		username = form.username.data

		user = User.query.filter_by(username=username).first()

		if user:
			if user.check_password(form.password.data):
				flash("Successful login!")
				login_user(user)
				return redirect('/')
			else:
				flash("Failed login")
		else:
			flash("Failed login")

	return render_template('login.html', title="Login", form=form)

@myapp_obj.route('/register', methods=['GET','POST'])
def register():
	form = SignUpForm()
	if form.validate_on_submit():
		username = form.username.data

		user = User.query.filter_by(username=username).first()

		if not user:
			u = User(username=username)
			u.set_password(form.password.data)
			db.session.add(u)
			db.session.commit()
			return redirect('/login')
		else:
			flash("User already exists")

	return render_template('login.html', title='Register', form=form)

@myapp_obj.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect('/login')

@myapp_obj.route('/home')
@login_required
def home():
	return 'home'

#Displaying images on a page seems to involve setting a landing page which has an embedded GET request for the appropriate imag

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@myapp_obj.route('/')
def upload_form():
	return render_template('upload.html')

@myapp_obj.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		if not os.path.exists(myapp_obj.config['UPLOAD_FOLDER']):
			os.makedirs(myapp_obj.config['UPLOAD_FOLDER'])
		file.save(os.path.join(myapp_obj.config['UPLOAD_FOLDER'], filename))
		print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below')
		return render_template('upload.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@myapp_obj.route('/display/<filename>')
def display_image(filename):
	print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)
