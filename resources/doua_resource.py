from flask import Blueprint, request
from models.doua import Doua
from models.favorite_doua import FavoriteDoua
from models.db import db
from schemas import DouaSchema, FavoriteDouaSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
# IMPORTANT: blueprint name does NOT affect URL, but keep it clean
doua_bp = Blueprint("doua_bp", __name__)

doua_schema = DouaSchema()
doua_list_schema = DouaSchema(many=True)
fav_schema = FavoriteDouaSchema()
fav_list_schema = FavoriteDouaSchema(many=True)




# ✅ GET ALL DOUA
@doua_bp.route("/", methods=["GET"])
def get_all_doua():
    doua = Doua.query.all()
    return doua_list_schema.dump(doua), 200


# ✅ GET BY NAME
@doua_bp.route("/name/<string:esm>", methods=["GET"])
def get_doua_by_name(esm):
    doua = Doua.query.filter_by(name_latin=esm).all()
    return doua_list_schema.dump(doua), 200


# 🔐 ADD FAVORITE
@doua_bp.route("/favorite", methods=["POST"])
@jwt_required()
def add_favorite():
    user_id = get_jwt_identity()
    data = request.get_json()

    doua = Doua.query.get(data["doua_id"])
    if not doua:
        return {"error": "Doua not found"}, 404

    fav = FavoriteDoua(
        user_id=user_id,
        doua_id=data["doua_id"]
    )

    db.session.add(fav)
    db.session.commit()

    return fav_schema.dump(fav), 201

# 🔐 DELETE FAVORITE
@doua_bp.route("/favorite/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_favorite(id):
    user_id = get_jwt_identity()

    fav = FavoriteDoua.query.filter_by(id=id, user_id=user_id).first_or_404()
    db.session.delete(fav)
    db.session.commit()

    return {"message": "Favorite deleted"}, 200

# 🔐 GET USER FAVORITES (FULL DOUA)
@doua_bp.route("/favorite", methods=["GET"])
@jwt_required()
def get_my_favorites():
    user_id = get_jwt_identity()

    favs = FavoriteDoua.query.filter_by(user_id=user_id).all()
    return fav_list_schema.dump(favs), 200