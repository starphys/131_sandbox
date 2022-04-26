from app import myapp_obj, db, basedir
from app.forms import AuctionForm, LoginForm, SignUpForm, ListingForm
from app.models import Bid, Listing, User
from flask import redirect, render_template, flash, request, url_for
from flask_login import current_user, login_user, logout_user, login_required

import os
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@myapp_obj.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data

        user = User.query.filter_by(username=username).first()

        if user:
            if user.check_password(form.password.data):
                flash("Successful login!")
                login_user(user)
                return redirect("/")
            else:
                flash("Failed login")
        else:
            flash("Failed login")

    return render_template("login.html", title="Login", form=form)


@myapp_obj.route("/register", methods=["GET", "POST"])
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
            return redirect("/login")
        else:
            flash("User already exists")

    return render_template("login.html", title="Register", form=form)


@myapp_obj.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@myapp_obj.route("/")
@login_required
def home():
    return "home"


@myapp_obj.route("/newlisting", methods=["GET", "POST"])
@login_required
def upload_form():
    form = ListingForm()

    if form.validate_on_submit():
        if not form.image.data:
            flash("Please select an image")
            return redirect(request.url)

        file = form.image.data
        if file.filename == "":
            flash("Please select an image")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            if not os.path.exists(myapp_obj.config["UPLOAD_FOLDER"]):
                os.makedirs(myapp_obj.config["UPLOAD_FOLDER"])

            file.save(os.path.join(myapp_obj.config["UPLOAD_FOLDER"], filename))

            l = Listing(
                title=form.title.data,
                description=form.description.data,
                image=filename,
                biddable=form.biddable.data,
                buyable=form.buyable.data,
                price=form.price.data,
                seller=current_user,
            )
            db.session.add(l)
            db.session.commit()

            listing = Listing.query.filter_by(image=filename)[0]
            print(listing)

            return render_template(
                "newlisting.html",
                title="New Listing",
                form=form,
                filename=listing.image,
            )
        else:
            flash("Allowed image types are png, jpg, jpeg, and gif")
            return redirect(request.url)
    return render_template("newlisting.html", title="New Listing", form=form)


@myapp_obj.route("/display/<filename>")
@login_required
def display_image(filename):
    return redirect(url_for("static", filename="images/" + filename), code=301)


@myapp_obj.route("/listing/<listing_id>", methods=["GET", "POST"])
def display_listing(listing_id):
    listing = Listing.query.filter_by(id=listing_id).first()

    if listing is not None:
        if listing.biddable:
            form = AuctionForm()
            highest_bid = listing.bids.order_by(Bid.value.desc()).first()

            if highest_bid is None:
                highest_bid = Bid(value=0.00)

            if form.validate_on_submit():
                if form.price.data <= highest_bid.value:
                    flash(
                        "${:,.2f} is not larger than the highest bid.".format(
                            form.price.data
                        )
                    )
                else:
                    b = Bid(
                        value=form.price.data,
                        bidder=current_user,
                        listing_id=listing_id,
                    )
                    db.session.add(b)
                    db.session.commit()
                    highest_bid = listing.bids.order_by(Bid.value.desc()).first()

            return render_template(
                "listing.html",
                title=listing.title,
                description=listing.description,
                filename=listing.image,
                price="${:,.2f}".format(listing.price),
                accepts_bids=listing.biddable,
                form=form,
                highest_bid="${:,.2f}".format(highest_bid.value),
            )
        else:
            return render_template(
                "listing.html",
                title=listing.title,
                description=listing.description,
                filename=listing.image,
                price="${:,.2f}".format(listing.price),
                accepts_bids=listing.biddable,
            )
    return redirect("/")
