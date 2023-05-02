"""Flask app for Cupcakes"""

import os
from flask import Flask, jsonify, request, render_template
from models import db, Cupcake, connect_db, DEFAULT_IMAGE_URL

app = Flask(__name__)
app.debug = True

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///cupcakes")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.get('/')
def homepage():
    """ """
    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return render_template("homepage.html")


@app.get('/api/cupcakes')
def list_all_cupcakes():
    """Return JSON {'cupcakes': [{id, flavor, size, rating, image_url}, ...]}"""

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get('/api/cupcakes/<cupcake_id>')
def list_single_cupcake(cupcake_id):
    """Return JSON {'cupcake': {id, flavor, size, rating, image_url}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
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
    image_url = request.json.get("image_url") or None

    new_cupcake = Cupcake(flavor=flavor,
                          size=size,
                          rating=rating,
                          image_url=image_url)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)



@app.patch('/api/cupcakes/<cupcake_id>')
def update_cupcake(cupcake_id):
    """Update instance of Cupcake by changing 1 or more values,
    return JSON {cupcake: {id, flavor, size, rating, image_url}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    if "image_url" in request.json:
        cupcake.image_url = request.json.get("image_url") or DEFAULT_IMAGE_URL

    db.session.commit()

    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.delete('/api/cupcakes/<int:cupcake_id>')
def delete_cupcake(cupcake_id):
    """Delete instance of Cupcake,
    return JSON {cupcake: {id, flavor, size, rating, image_url}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify({"deleted": cupcake_id})