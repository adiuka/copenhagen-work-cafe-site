from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from flask_bootstrap import Bootstrap5
from forms import CreateCafeForm
import os
import random


app = Flask(__name__)


# Create DB
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///copenhagen_cafes.db'
app.config['SECRET_KEY'] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
db = SQLAlchemy(model_class=Base)
Bootstrap5(app)
db.init_app(app)


class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    vegan_options: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


# Initialise the database
with app.app_context():
    db.create_all()

# WEBSITE ROUTES USER UI
@app.route('/')
def render_home():
    """ Renders the homepage and filters it based on selections """
    selected_filters = request.args.getlist('filters', None) # Get the filter from the url

    cafes = Cafe.query.all()

    if 'has_wifi' in selected_filters:
        cafes = [cafe for cafe in cafes if cafe.has_wifi]
    if 'has_toilet' in selected_filters:
        cafes = [cafe for cafe in cafes if cafe.has_toilet]
    if 'has_sockets' in selected_filters:
        cafes = [cafe for cafe in cafes if cafe.has_sockets]
    if 'vegan_options' in selected_filters:
        cafes = [cafe for cafe in cafes if cafe.vegan_options]

    return render_template("index.html", all_cafes=cafes, selected_filters=selected_filters)


@app.route("/all")
def get_all_cafes():
    """Primarily an imitation of an API, returns all cafes in JSON. Work in Progress"""
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route("/cafe/<int:cafe_id>")
def show_cafe(cafe_id):
    """ Renders the selected cafe based on the one you click """
    requested_cafe = db.get_or_404(Cafe, cafe_id)
    return render_template("cafe.html", cafe=requested_cafe)


@app.route("/new-cafe", methods=["GET", "POST"])
def new_cafe():
    """ The Approute that creates a WTForm for a user to enter their new Cafe """
    form = CreateCafeForm()

    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            seats=form.seats.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            has_sockets=form.has_sockets.data,
            vegan_options=form.vegan_options.data,
            coffee_price=form.coffee_price.data + " kr",
        )

        db.session.add(new_cafe)
        db.session.commit()
        flash("Cafe Added Successfully!", "success")
        return redirect(url_for('render_home')) # Redirects to the homepage
    
    return render_template("add_cafe.html", form=form)


@app.route("/delete_cafe/<int:cafe_id>", methods=["POST"])
def delete_cafe(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)

    if cafe_to_delete:
        db.session.delete(cafe_to_delete)
        db.session.commit()
        flash("Cafe Deleted Successfully", "success")
    
    else:
        flash("Cafe Not Found", "danger")

    return redirect(url_for("render_home"))


# API ROUTES for POSTMAN
@app.route("/add", methods=["POST"])
def post_new_cafe():
    """The approute that works together with Postman to create a New Cafe"""
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        seats=request.form.get("seats"),
        has_toilet=bool(request.form.get("has_toilet")),
        has_wifi=bool(request.form.get("has_wifi")),
        has_sockets=bool(request.form.get("has_sockets")),
        vegan_options=bool(request.form.get("vegan_options")),
        coffee_price=request.form.get("coffee_price") + " kr",
    )
    db.session.add(new_cafe)
    db.session.commit()

    return jsonify(response={"success": "Successfully added the new cafe"})


@app.route("/closed/<int:cafe_id>")
def close_cafe(cafe_id):
    """The function that communicates with the API to delete a Cafe"""
    cafe = db.get_or_404(Cafe, cafe_id)
    if cafe:
        db.session.delete(cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    


if __name__ == '__main__':
    app.run(debug=True, port=5001)
