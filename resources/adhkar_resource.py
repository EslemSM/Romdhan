from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.adhkar import Adhkar
from models.favorite_adhkar import FavoriteAdhkar
from models.db import db
from schemas import AdhkarSchema, FavoriteAdhkarSchema


adhkar_bp = Blueprint('adhkar', __name__, "Remembering Allah")

adhkar_schema = AdhkarSchema()
adhkar_list_schema = AdhkarSchema(many=True)
fav_schema = FavoriteAdhkarSchema()
fav_list_schema = FavoriteAdhkarSchema(many=True)


@adhkar_bp.route('/', methods=['GET'])
def get_all_adhkar():
    adhkar = Adhkar.query.order_by(Adhkar.category).all()
    return adhkar_list_schema.dump(adhkar), 200


@adhkar_bp.route('/<string:category>', methods=['GET'])
def get_adhkar_by_category(category):
    adhkar = Adhkar.query.filter_by(category=category).all()
    return adhkar_list_schema.dump(adhkar), 200


# 🔐 ADD FAVORITE
@adhkar_bp.route("/favorite", methods=["POST"])
@jwt_required()
def add_favorite():
    user_id = get_jwt_identity()
    data = request.get_json()

    adhkar = Adhkar.query.get(data["adhkar_id"])
    if not adhkar:
        return {"error": "Adhkar not found"}, 404

    fav = FavoriteAdhkar(
        user_id=user_id,
        adhkar_id=data["adhkar_id"]
    )

    db.session.add(fav)
    db.session.commit()

    return fav_schema.dump(fav), 201


# 🔐 DELETE FAVORITE
@adhkar_bp.route("/favorite/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_favorite(id):
    user_id = get_jwt_identity()

    fav = FavoriteAdhkar.query.filter_by(id=id, user_id=user_id).first_or_404()
    db.session.delete(fav)
    db.session.commit()

    return {"message": "Favorite removed"}, 200


# 🔐 GET USER FAVORITES (FULL ADHKAR)
@adhkar_bp.route("/favorite", methods=["GET"])
@jwt_required()
def get_my_favorites():
    user_id = get_jwt_identity()

    favs = FavoriteAdhkar.query.filter_by(user_id=user_id).all()
    return fav_list_schema.dump(favs), 200



# 🔐 GET USER FAVORITES BY CATEGORY (PROTECTED)
@adhkar_bp.route('/favorite/category/<string:category>', methods=['GET'])
@jwt_required()
def get_favorite_by_category(category):
    # Get the authenticated user's ID
    user_id = get_jwt_identity()
    
    # Filter favorites by both user_id AND category
    favs = (
        FavoriteAdhkar.query
        .join(Adhkar)
        .filter(
            FavoriteAdhkar.user_id == user_id,
            Adhkar.category == category
        )
        .all()
    )
    
    return fav_list_schema.dump(favs), 200
