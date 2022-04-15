from app import myapp_obj, db
from app.forms import LoginForm, SignUpForm
from app.models import User
from flask import redirect, render_template, flash
from flask_login import current_user, login_user, logout_user, login_required


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

@myapp_obj.route('/')
@login_required
def home():
    return 'home'

