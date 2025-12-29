from flask import Blueprint, request
from models.adhkar import Adhkar
from models.favorite_adhkar import FavoriteAdhkar
from models.db import db
from schemas import AdhkarSchema, FavoriteAdhkarSchema

adhkar_bp = Blueprint('adhkar', __name__)

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


@adhkar_bp.route('/favorite', methods=['POST'])
def add_favorite():
    data = request.get_json()
    fav = FavoriteAdhkar(**data)
    db.session.add(fav)
    db.session.commit()
    return fav_schema.dump(fav), 201


@adhkar_bp.route('/favorite/<int:id>', methods=['DELETE'])
def delete_favorite(id):
    fav = FavoriteAdhkar.query.get_or_404(id)
    db.session.delete(fav)
    db.session.commit()
    return {"message": "Favorite removed"}, 200


@adhkar_bp.route('/favorite', methods=['GET'])
def get_all_favorites():
    favs = FavoriteAdhkar.query.all()
    return fav_list_schema.dump(favs), 200


@adhkar_bp.route('/favorite/category/<string:category>', methods=['GET'])
def get_favorite_by_category(category):
    favs = FavoriteAdhkar.query.join(Adhkar).filter(Adhkar.category == category).all()
    return fav_list_schema.dump(favs), 200
