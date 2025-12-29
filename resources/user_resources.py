from flask import Blueprint, request
from models.user import User
from models.db import db
from schemas import UserSchema

user_bp = Blueprint('users', __name__)

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)


@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data.get("username"):
        return {"error": "username required"}, 400

    user = User(
        username=data['username'],
        password_hash="temp_password"
    )

    db.session.add(user)
    db.session.commit()

    return user_schema.dump(user), 201


@user_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return user_list_schema.dump(users), 200
