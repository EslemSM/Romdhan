
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required
from models.user import User
from models.db import db
from schemas import UserSchema, UserRegisterSchema, UserLoginSchema, TokenSchema
from flask_jwt_extended import get_jwt_identity

user_bp = Blueprint("users", __name__)

user_schema = UserSchema()
user_register_schema = UserRegisterSchema()
user_login_schema = UserLoginSchema()
token_schema = TokenSchema()

# 🟢 REGISTER
# 🟢 REGISTER (with optional password length check)
@user_bp.route("/register", methods=["POST"])
def register():
    try:
        # Validate input with UserRegisterSchema
        data = user_register_schema.load(request.get_json())
        
        if User.query.filter_by(username=data["username"]).first():
            return {"error": "User already exists"}, 409

        user = User(username=data["username"])
        user.set_password(data["password"])  # Now uses pbkdf2_sha256

        db.session.add(user)
        db.session.commit()

        # Return user data with UserSchema
        return user_schema.dump(user), 201
    except ValueError as e:  # Catch password validation errors from model
        return {"error": str(e)}, 400
    except Exception as e:
        db.session.rollback()
        return {"error": f"Registration failed: {str(e)}"}, 500
# 🔐 LOGIN
@user_bp.route("/login", methods=["POST"])
def login():
    try:
        # Validate input with UserLoginSchema
        data = user_login_schema.load(request.get_json())

        user = User.query.filter_by(username=data["username"]).first()
        if not user or not user.check_password(data["password"]):
            return {"error": "Invalid credentials"}, 401

        access_token = create_access_token(identity=str(user.id))

        # Return token with TokenSchema, plus user data
        return {
            "access_token": token_schema.dump({"access_token": access_token})["access_token"],
            "user": user_schema.dump(user)
        }, 200
    except Exception as e:
        return {"error": f"Login failed: {str(e)}"}, 500

# 🔓 LOGOUT (Client-side: Delete the token)
@user_bp.route("/logout", methods=["POST"])
@jwt_required()  # Requires valid token
def logout():
    # JWT is stateless, so logout is client-side (delete token).
    return {"message": "Logged out successfully. Please delete your access token."}, 200

# (Optional) List users — for testing only (protected)
@user_bp.route("/", methods=["GET"])
@jwt_required()  # Protect with JWT
def get_users():
    users = User.query.all()
    return user_schema.dump(users, many=True), 200
