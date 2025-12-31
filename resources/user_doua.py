from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user_doua import UserDoua
from models.db import db
from schemas import UserDouaSchema

user_doua_bp = Blueprint("user_doua", __name__)

schema = UserDouaSchema()
list_schema = UserDouaSchema(many=True)


# 🔐 CREATE
@user_doua_bp.route("/", methods=["POST"])
@jwt_required()
def create_user_doua():
    user_id = get_jwt_identity()
    data = request.get_json()

    doua = UserDoua(
        user_id=user_id,
        title=data.get("title"),
        text_ar=data["text_ar"],
        text_latin=data.get("text_latin"),
        category=data.get("category")
    )

    db.session.add(doua)
    db.session.commit()

    return schema.dump(doua), 201


# 🔐 GET ALL
@user_doua_bp.route("/", methods=["GET"])
@jwt_required()
def get_user_doua():
    user_id = get_jwt_identity()
    doua = UserDoua.query.filter_by(user_id=user_id).all()
    return list_schema.dump(doua), 200


# 🔐 GET BY CATEGORY
@user_doua_bp.route("/category/<string:category>", methods=["GET"])
@jwt_required()
def get_user_doua_by_category(category):
    user_id = get_jwt_identity()

    doua = UserDoua.query.filter_by(
        user_id=user_id,
        category=category
    ).all()

    return list_schema.dump(doua), 200



# 🔐 PUT
@user_doua_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_user_doua(id):
    user_id = get_jwt_identity()
    data = request.get_json()

    doua = UserDoua.query.filter_by(id=id, user_id=user_id).first_or_404()

    doua.title = data.get("title")
    doua.text_ar = data["text_ar"]
    doua.text_latin = data.get("text_latin")
    doua.category = data.get("category")

    db.session.commit()
    return schema.dump(doua), 200


# 🔐 PATCH
@user_doua_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def patch_user_doua(id):
    user_id = get_jwt_identity()
    data = request.get_json()

    doua = UserDoua.query.filter_by(id=id, user_id=user_id).first_or_404()

    if "title" in data:
        doua.title = data["title"]
    if "text_ar" in data:
        doua.text_ar = data["text_ar"]
    if "text_latin" in data:
        doua.text_latin = data["text_latin"]
    if "category" in data:
        doua.category = data["category"]

    db.session.commit()
    return schema.dump(doua), 200


# 🔐 DELETE
@user_doua_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user_doua(id):
    user_id = get_jwt_identity()
    doua = UserDoua.query.filter_by(id=id, user_id=user_id).first_or_404()

    db.session.delete(doua)
    db.session.commit()

    return {"message": "User doua deleted"}, 200
