from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, BooleanField
from wtforms.validators import DataRequired, URL


# The form to create a new Cafe Entry
class CreateCafeForm(FlaskForm):
    # String Fields
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = URLField("Map Link", validators=[DataRequired(), URL()])
    img_url = URLField("Image Link", validators=[DataRequired(), URL()])
    location = StringField("District", validators=[DataRequired()])
    seats = StringField("Seats", validators=[DataRequired()])
    coffee_price = StringField("Price for a Coffee", validators=[DataRequired()])

    # Boolean Fields
    has_toilet = BooleanField("Has Toilet")
    has_wifi = BooleanField("Has WiFi")
    has_sockets = BooleanField("Has Power Outlets")
    vegan_options = BooleanField("Vegan Options")
    

    # Submit
    submit = SubmitField("Add Cafe")
