from flask import Blueprint, request
from models.doua import Doua
from models.favorite_doua import FavoriteDoua
from models.db import db
from schemas import DouaSchema, FavoriteDouaSchema

# IMPORTANT: blueprint name does NOT affect URL, but keep it clean
doua_bp = Blueprint("doua_bp", __name__)

doua_schema = DouaSchema()
doua_list_schema = DouaSchema(many=True)
fav_schema = FavoriteDouaSchema()
fav_list_schema = FavoriteDouaSchema(many=True)


# ✅ TEST ROUTE
@doua_bp.route("/test", methods=["GET"])
def test_doua():
    return {"ok": True}, 200


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


# ✅ ADD FAVORITE (TEMP: no auth yet)
@doua_bp.route("/favorite", methods=["POST"])
def add_favorite():
    data = request.get_json()

    if not data.get("user_id") or not data.get("doua_id"):
        return {"error": "user_id and doua_id required"}, 400

    doua = Doua.query.get(data["doua_id"])
    if not doua:
        return {"error": "Doua not found"}, 404

    fav = FavoriteDoua(
        user_id=data["user_id"],
        doua_id=data["doua_id"]
    )

    db.session.add(fav)
    db.session.commit()

    return fav_schema.dump(fav), 201


# ✅ DELETE FAVORITE
@doua_bp.route("/favorite/<int:id>", methods=["DELETE"])
def delete_favorite(id):
    fav = FavoriteDoua.query.get_or_404(id)
    db.session.delete(fav)
    db.session.commit()
    return {"message": "Favorite deleted"}, 200


# ✅ GET ALL FAVORITES
@doua_bp.route("/favorite", methods=["GET"])
def get_all_favorites():
    favs = FavoriteDoua.query.all()
    return fav_list_schema.dump(favs), 200
