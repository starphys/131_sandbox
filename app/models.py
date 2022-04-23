from app import db
from datetime import datetime
from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    listings = db.relationship("Listing", backref="seller", lazy="dynamic")
    bids = db.relationship("Bid", backref="bids", lazy="dynamic")

    def __repr__(self):
        return f"<User = {self.username}, {self.email}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    title = db.Column(db.String(128))
    description = db.Column(db.String(256))
    image = db.Column(db.String(256))
    biddable = db.Column(db.Boolean, default=False)
    price = db.Column(
        db.Integer
    )  # stored as an integer in cents to avoid floating point errors.

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    bids = db.relationship("Bid", backref="bids", lazy="dynamic")

    def __repr__(self):
        image = True
        if self.image == "":
            image = False
        return f"<Listing: {self.id}, {self.timestamp}, {self.title}, {self.description}, {image}, {self.user_id}>"


class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    value = db.Column(
        db.Integer
    )  # stored as an integer in cents to avoid floating point errors.
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    listing_id = db.Column(db.Integer, db.ForeignKey("listing.id"))

    def __repr__(self):
        return f"<Bid: {self.id}, {self.timestamp}, {self.value}, {self.user_id}, {self.listing_id}>"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
