from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)
db_file = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_DATABASE_URI"] = db_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json() or {}
    name = data.get("name")
    description = data.get("description", "")
    if not name:
        return jsonify({"error": "name is required"}), 400
    item = Item(name=name, description=description)
    try:
        db.session.add(item)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "item with that name already exists3"}), 400
    return jsonify(item.to_dict()), 201

@app.route("/items", methods=["GET"])
def list_items():
    items = Item.query.all()
    return jsonify([i.to_dict() for i in items]), 200

@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify(item.to_dict()), 200

@app.route("/items/<int:item_id>", methods=["PUT", "PATCH"])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.get_json() or {}
    name = data.get("name")
    description = data.get("description")
    if name:
        item.name = name
    if description is not None:
        item.description = description
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "item with that name already exists"}), 400
    return jsonify(item.to_dict()), 200

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
