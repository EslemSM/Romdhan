from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields

from models.adhkar import Adhkar
from models.favorite_adhkar import FavoriteAdhkar
from models.db import db
from schemas import AdhkarSchema, FavoriteAdhkarSchema

# -------------------------------------------------------------------
# Blueprint
# -------------------------------------------------------------------
adhkar_bp = Blueprint(
    "adhkar_bp",
    __name__,
    description="Remembering Allah"
)

# -------------------------------------------------------------------
# Schemas (MUST be defined before routes)
# -------------------------------------------------------------------
adhkar_schema = AdhkarSchema()
adhkar_list_schema = AdhkarSchema(many=True)

fav_schema = FavoriteAdhkarSchema()
fav_list_schema = FavoriteAdhkarSchema(many=True)

# Input schema for POST /favorite
class FavoriteAdhkarCreateSchema(Schema):
    adhkar_id = fields.Int(required=True)


# -------------------------------------------------------------------
# Public endpoints (NO JWT)
# -------------------------------------------------------------------

@adhkar_bp.route('/', methods=['GET'])
@adhkar_bp.response(200, adhkar_list_schema)
def get_all_adhkar():
    """Get all Adhkar (ordered by category)"""
    adhkar = Adhkar.query.order_by(Adhkar.category).all()
    return adhkar


# use '/category/<category>' to avoid route collision with '/favorite'
@adhkar_bp.route('/category/<string:category>', methods=['GET'])
@adhkar_bp.response(200, adhkar_list_schema)
def get_adhkar_by_category(category):
    """Get Adhkar by category"""
    adhkar = Adhkar.query.filter_by(category=category).all()
    return adhkar


# -------------------------------------------------------------------
# Protected endpoints (JWT REQUIRED 🔐)
# -------------------------------------------------------------------

@adhkar_bp.route("/favorite", methods=["POST"])
@adhkar_bp.doc(security=[{"bearerAuth": []}])
@adhkar_bp.arguments(FavoriteAdhkarCreateSchema, location="json")
@adhkar_bp.response(201, fav_schema)
@jwt_required()
def add_favorite(data):
    """Add Adhkar to user favorites"""
    user_id = get_jwt_identity()

    adhkar = Adhkar.query.get(data["adhkar_id"])
    if not adhkar:
        abort(404, message="Adhkar not found")

    fav = FavoriteAdhkar(
        user_id=user_id,
        adhkar_id=data["adhkar_id"]
    )

    db.session.add(fav)
    db.session.commit()

    return fav


@adhkar_bp.route("/favorite/<int:id>", methods=["DELETE"])
@adhkar_bp.doc(security=[{"bearerAuth": []}])
@adhkar_bp.response(200)
@jwt_required()
def delete_favorite(id):
    """Remove Adhkar from favorites"""
    user_id = get_jwt_identity()

    fav = FavoriteAdhkar.query.filter_by(id=id, user_id=user_id).first()
    if not fav:
        abort(404, message="Favorite not found")

    db.session.delete(fav)
    db.session.commit()

    return {"message": "Favorite removed"}


@adhkar_bp.route("/favorite", methods=["GET"])
@adhkar_bp.doc(security=[{"bearerAuth": []}])
@adhkar_bp.response(200, fav_list_schema)
@jwt_required()
def get_my_favorites():
    """Get user's favorite Adhkar (full Adhkar objects via relationship/response schema)"""
    user_id = get_jwt_identity()

    favs = FavoriteAdhkar.query.filter_by(user_id=user_id).all()
    return favs


@adhkar_bp.route('/favorite/category/<string:category>', methods=['GET'])
@adhkar_bp.doc(security=[{"bearerAuth": []}])
@adhkar_bp.response(200, fav_list_schema)
@jwt_required()
def get_favorite_by_category(category):
    """Get user's favorite Adhkar filtered by category"""
    user_id = get_jwt_identity()

    favs = (
        FavoriteAdhkar.query
        .join(Adhkar)
        .filter(
            FavoriteAdhkar.user_id == user_id,
            Adhkar.category == category
        )
        .all()
    )

    return favs
