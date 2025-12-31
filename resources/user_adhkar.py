from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user_adhkar import UserAdhkar
from models.db import db
from schemas import UserAdhkarSchema

user_adhkar_bp = Blueprint("user_adhkar", __name__)

schema = UserAdhkarSchema()
list_schema = UserAdhkarSchema(many=True)


# 🔐 CREATE
@user_adhkar_bp.route("/", methods=["POST"])
@jwt_required()
def create_user_adhkar():
    user_id = get_jwt_identity()
    data = request.get_json()

    adhkar = UserAdhkar(
        user_id=user_id,
        text_ar=data["text_ar"],
        text_latin=data.get("text_latin"),
        category=data.get("category")
    )

    db.session.add(adhkar)
    db.session.commit()

    return schema.dump(adhkar), 201


# 🔐 GET ALL (current user)
@user_adhkar_bp.route("/", methods=["GET"])
@jwt_required()
def get_user_adhkar():
    user_id = get_jwt_identity()
    adhkar = UserAdhkar.query.filter_by(user_id=user_id).all()
    return list_schema.dump(adhkar), 200


# 🔐 GET BY CATEGORY
@user_adhkar_bp.route("/category/<string:category>", methods=["GET"])
@jwt_required()
def get_user_adhkar_by_category(category):
    user_id = get_jwt_identity()

    adhkar = UserAdhkar.query.filter_by(
        user_id=user_id,
        category=category
    ).all()

    return list_schema.dump(adhkar), 200

# 🔐 PUT (replace whole row)
@user_adhkar_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_user_adhkar(id):
    user_id = get_jwt_identity()
    data = request.get_json()

    adhkar = UserAdhkar.query.filter_by(id=id, user_id=user_id).first_or_404()

    adhkar.text_ar = data["text_ar"]
    adhkar.text_latin = data.get("text_latin")
    adhkar.category = data.get("category")

    db.session.commit()
    return schema.dump(adhkar), 200


# 🔐 PATCH (partial update)
@user_adhkar_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def patch_user_adhkar(id):
    user_id = get_jwt_identity()
    data = request.get_json()

    adhkar = UserAdhkar.query.filter_by(id=id, user_id=user_id).first_or_404()

    if "text_ar" in data:
        adhkar.text_ar = data["text_ar"]
    if "text_latin" in data:
        adhkar.text_latin = data["text_latin"]
    if "category" in data:
        adhkar.category = data["category"]

    db.session.commit()
    return schema.dump(adhkar), 200


# 🔐 DELETE
@user_adhkar_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user_adhkar(id):
    user_id = get_jwt_identity()
    adhkar = UserAdhkar.query.filter_by(id=id, user_id=user_id).first_or_404()

    db.session.delete(adhkar)
    db.session.commit()

    return {"message": "User adhkar deleted"}, 200
