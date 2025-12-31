from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields
from models.user_doua import UserDoua
from models.db import db
from schemas import UserDouaSchema

user_doua_bp = Blueprint(
    "user_doua",
    __name__,
    description="User custom Doua management"
)


doua_schema = UserDouaSchema()
doua_list_schema = UserDouaSchema(many=True)


class UserDouaCreateSchema(Schema):
    title = fields.Str()
    text_ar = fields.Str(required=True)
    text_latin = fields.Str()
    category = fields.Str()

class UserDouaUpdateSchema(Schema):
    title = fields.Str()
    text_ar = fields.Str(required=True)
    text_latin = fields.Str()
    category = fields.Str()

class UserDouaPatchSchema(Schema):
    title = fields.Str()
    text_ar = fields.Str()
    text_latin = fields.Str()
    category = fields.Str()



# CREATE

@user_doua_bp.route("/", methods=["POST"])
@user_doua_bp.doc(security=[{"bearerAuth": []}])
@user_doua_bp.arguments(UserDouaCreateSchema)
@user_doua_bp.response(201, doua_schema)
@jwt_required()
def create_user_doua(data):
    """Create a new dua for the authenticated user."""
    user_id = get_jwt_identity()

    doua = UserDoua(
        user_id=user_id,
        title=data.get("title"),
        text_ar=data["text_ar"],
        text_latin=data.get("text_latin"),
        category=data.get("category"),
    )

    db.session.add(doua)
    db.session.commit()

    return doua



# GET ALL (current user)

@user_doua_bp.route("/", methods=["GET"])
@user_doua_bp.doc(security=[{"bearerAuth": []}])
@user_doua_bp.response(200, doua_list_schema)
@jwt_required()
def get_user_doua():
    """Get all duas for the authenticated user."""
    user_id = get_jwt_identity()
    return UserDoua.query.filter_by(user_id=user_id).all()



#  GET BY CATEGORY

@user_doua_bp.route("/category/<string:category>", methods=["GET"])
@user_doua_bp.doc(security=[{"bearerAuth": []}])
@user_doua_bp.response(200, doua_list_schema)
@jwt_required()
def get_user_doua_by_category(category):
    """Get duas filtered by category."""
    user_id = get_jwt_identity()

    return UserDoua.query.filter_by(
        user_id=user_id,
        category=category
    ).all()



#  PUT (replace whole row)

@user_doua_bp.route("/<int:id>", methods=["PUT"])
@user_doua_bp.doc(security=[{"bearerAuth": []}])
@user_doua_bp.arguments(UserDouaUpdateSchema)
@user_doua_bp.response(200, doua_schema)
@jwt_required()
def update_user_doua(data, id):
    """Replace a dua completely."""
    user_id = get_jwt_identity()

    doua = UserDoua.query.filter_by(id=id, user_id=user_id).first_or_404()

    doua.title = data.get("title")
    doua.text_ar = data["text_ar"]
    doua.text_latin = data.get("text_latin")
    doua.category = data.get("category")

    db.session.commit()
    return doua



#  PATCH (partial update)

@user_doua_bp.route("/<int:id>", methods=["PATCH"])
@user_doua_bp.doc(security=[{"bearerAuth": []}])
@user_doua_bp.arguments(UserDouaPatchSchema)
@user_doua_bp.response(200, doua_schema)
@jwt_required()
def patch_user_doua(data, id):
    """Update one or more fields of a dua."""
    user_id = get_jwt_identity()

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
    return doua



#  DELETE

@user_doua_bp.route("/<int:id>", methods=["DELETE"])
@user_doua_bp.doc(security=[{"bearerAuth": []}])
@user_doua_bp.response(200)
@jwt_required()
def delete_user_doua(id):
    """Delete a dua."""
    user_id = get_jwt_identity()

    doua = UserDoua.query.filter_by(id=id, user_id=user_id).first_or_404()
    db.session.delete(doua)
    db.session.commit()

    return {"message": "User dua deleted"}
