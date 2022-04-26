from re import sub
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    DecimalField,
    IntegerField,
    DateField,
    DateTimeLocalField,
)
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")


class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")


class ListingForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    image = FileField("Image", validators=[FileRequired()])
    price = DecimalField("Purchase Price", places=2)
    biddable = BooleanField("Accept Bids")
    auction_end_time = DateField("Until")
    buyable = BooleanField("Available for Instant Purchase")
    submit = SubmitField("Create Listing")


class AuctionForm(FlaskForm):
    price = DecimalField("Price", places=2, validators=[DataRequired()])
    submit = SubmitField("Place Your Bid")


class CreditCardForm(FlaskForm):
    number = StringField(
        "Credit Card Number", validators=[DataRequired(), Length(min=16, max=16)]
    )
    name = StringField("Name on Card", validators=[DataRequired()])
    expire_date = DateField("Expiration Date", validators=[DataRequired()])
    cvv = StringField("CVV", validators=[DataRequired(), Length(min=3, max=3)])
    submit = SubmitField("Confirm Purchase")
