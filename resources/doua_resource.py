from flask_smorest import Blueprint, abort
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields

from models.doua import Doua
from models.favorite_doua import FavoriteDoua
from models.db import db
from schemas import DouaSchema, FavoriteDouaSchema

# -------------------------------------------------------------------
# Blueprint
# -------------------------------------------------------------------
doua_bp = Blueprint(
    "doua_bp",
    __name__,
    description="Get Doua by calling Allah's name"
)

# -------------------------------------------------------------------
# Schemas (MUST be defined before routes)
# -------------------------------------------------------------------
doua_schema = DouaSchema()
doua_list_schema = DouaSchema(many=True)

fav_schema = FavoriteDouaSchema()
fav_list_schema = FavoriteDouaSchema(many=True)

# Input schema for POST /favorite
class FavoriteCreateSchema(Schema):
    doua_id = fields.Int(required=True)


# -------------------------------------------------------------------
# Public endpoints (NO JWT)
# -------------------------------------------------------------------

@doua_bp.route("/", methods=["GET"])
@doua_bp.response(200, doua_list_schema)
def get_all_doua():
    """Get all Doua"""
    doua = Doua.query.all()
    return doua


@doua_bp.route("/name/<string:esm>", methods=["GET"])
@doua_bp.response(200, doua_list_schema)
def get_doua_by_name(esm):
    """Get Doua by latin name"""
    doua = Doua.query.filter_by(name_latin=esm).all()
    return doua


# -------------------------------------------------------------------
# Protected endpoints (JWT REQUIRED 🔐)
# -------------------------------------------------------------------

@doua_bp.route("/favorite", methods=["POST"])
@doua_bp.doc(security=[{"bearerAuth": []}])
@doua_bp.arguments(FavoriteCreateSchema)
@doua_bp.response(201, fav_schema)
@jwt_required()
def add_favorite(data):
    """Add Doua to user favorites"""
    user_id = get_jwt_identity()

    doua = Doua.query.get(data["doua_id"])
    if not doua:
        abort(404, message="Doua not found")

    fav = FavoriteDoua(
        user_id=user_id,
        doua_id=data["doua_id"]
    )

    db.session.add(fav)
    db.session.commit()

    return fav


@doua_bp.route("/favorite/<int:id>", methods=["DELETE"])
@doua_bp.doc(security=[{"bearerAuth": []}])
@doua_bp.response(200)
@jwt_required()
def delete_favorite(id):
    """Remove Doua from favorites"""
    user_id = get_jwt_identity()

    fav = FavoriteDoua.query.filter_by(
        id=id,
        user_id=user_id
    ).first()

    if not fav:
        abort(404, message="Favorite not found")

    db.session.delete(fav)
    db.session.commit()

    return {"message": "Favorite deleted"}


@doua_bp.route("/favorite", methods=["GET"])
@doua_bp.doc(security=[{"bearerAuth": []}])
@doua_bp.response(200, fav_list_schema)
@jwt_required()
def get_my_favorites():
    """Get user's favorite Doua"""
    user_id = get_jwt_identity()

    favs = FavoriteDoua.query.filter_by(user_id=user_id).all()
    return favs
