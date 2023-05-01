"""Flask app for Cupcakes"""

import os
from flask import Flask, jsonify, request
from models import db, Cupcake, connect_db

app = Flask(__name__)
app.debug = True

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///cupcakes")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.get('/api/cupcakes')
def list_all_cupcakes():
    """Return JSON {'cupcakes': [{id, flavor, size, rating, image_url}, ...]}"""

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get('api/cupcakes/<cupcake-id>')
def list_single_cupcake():
    """Return JSON {'cupcake': {id, flavor, size, rating, image_url}}"""

    cupcake = Cupcake.query.get_or_404(cupcake-id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.post('/api/cupcakes')
def create_cupcake():
    """Create instance of Cupcake,
    return JSON {cupcake: {id, flavor, size, rating, image_url}}
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image_url = request.json["image_url"]

    new_cupcake = Cupcake(flavor=flavor,
                          size=size,
                          rating=rating,
                          image_url=image_url)

    db.session.add(new_cupcake)
    db.session.commit

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)

