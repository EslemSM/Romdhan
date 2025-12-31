from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields
from models.user_adhkar import UserAdhkar
from models.db import db
from schemas import UserAdhkarSchema


user_adhkar_bp = Blueprint(
    "user_adhkar",
    __name__,
    description="User custom Adhkar management"
)


adhkar_schema = UserAdhkarSchema()
adhkar_list_schema = UserAdhkarSchema(many=True)

class UserAdhkarCreateSchema(Schema):
    text_ar = fields.Str(required=True)
    text_latin = fields.Str()
    category = fields.Str()

class UserAdhkarUpdateSchema(Schema):
    text_ar = fields.Str(required=True)
    text_latin = fields.Str()
    category = fields.Str()

class UserAdhkarPatchSchema(Schema):
    text_ar = fields.Str()
    text_latin = fields.Str()
    category = fields.Str()

@user_adhkar_bp.route("/", methods=["POST"])
@user_adhkar_bp.doc(security=[{"bearerAuth": []}])
@user_adhkar_bp.arguments(UserAdhkarCreateSchema)
@user_adhkar_bp.response(201, adhkar_schema)
@jwt_required()
def create_user_adhkar(data):
    """Create a new adhkar for the authenticated user."""
    user_id = get_jwt_identity()

    adhkar = UserAdhkar(
        user_id=user_id,
        text_ar=data["text_ar"],
        text_latin=data.get("text_latin"),
        category=data.get("category"),
    )

    db.session.add(adhkar)
    db.session.commit()

    return adhkar



#  GET ALL (current user)

@user_adhkar_bp.route("/", methods=["GET"])
@user_adhkar_bp.doc(security=[{"bearerAuth": []}])
@user_adhkar_bp.response(200, adhkar_list_schema)
@jwt_required()
def get_user_adhkar():
    """Get all adhkar for the authenticated user."""
    user_id = get_jwt_identity()
    return UserAdhkar.query.filter_by(user_id=user_id).all()



# GET BY CATEGORY

@user_adhkar_bp.route("/category/<string:category>", methods=["GET"])
@user_adhkar_bp.doc(security=[{"bearerAuth": []}])
@user_adhkar_bp.response(200, adhkar_list_schema)
@jwt_required()
def get_user_adhkar_by_category(category):
    """Get adhkar filtered by category."""
    user_id = get_jwt_identity()

    return UserAdhkar.query.filter_by(
        user_id=user_id,
        category=category
    ).all()



# PUT (replace whole row)

@user_adhkar_bp.route("/<int:id>", methods=["PUT"])
@user_adhkar_bp.doc(security=[{"bearerAuth": []}])
@user_adhkar_bp.arguments(UserAdhkarUpdateSchema)
@user_adhkar_bp.response(200, adhkar_schema)
@jwt_required()
def update_user_adhkar(data, id):
    """Replace an adhkar completely."""
    user_id = get_jwt_identity()

    adhkar = UserAdhkar.query.filter_by(id=id, user_id=user_id).first_or_404()

    adhkar.text_ar = data["text_ar"]
    adhkar.text_latin = data.get("text_latin")
    adhkar.category = data.get("category")

    db.session.commit()
    return adhkar


#  PATCH (partial update)
@user_adhkar_bp.route("/<int:id>", methods=["PATCH"])
@user_adhkar_bp.doc(security=[{"bearerAuth": []}])
@user_adhkar_bp.arguments(UserAdhkarPatchSchema)
@user_adhkar_bp.response(200, adhkar_schema)
@jwt_required()
def patch_user_adhkar(data, id):
    """Update one or more fields of an adhkar."""
    user_id = get_jwt_identity()

    adhkar = UserAdhkar.query.filter_by(id=id, user_id=user_id).first_or_404()

    if "text_ar" in data:
        adhkar.text_ar = data["text_ar"]
    if "text_latin" in data:
        adhkar.text_latin = data["text_latin"]
    if "category" in data:
        adhkar.category = data["category"]

    db.session.commit()
    return adhkar



# DELETE
@user_adhkar_bp.route("/<int:id>", methods=["DELETE"])
@user_adhkar_bp.doc(security=[{"bearerAuth": []}])
@user_adhkar_bp.response(200)
@jwt_required()
def delete_user_adhkar(id):
    """Delete an adhkar."""
    user_id = get_jwt_identity()

    adhkar = UserAdhkar.query.filter_by(id=id, user_id=user_id).first_or_404()
    db.session.delete(adhkar)
    db.session.commit()

    return {"message": "User adhkar deleted"}
