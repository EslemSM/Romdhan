from marshmallow import Schema
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, jwt_required
from models.user import User
from models.db import db
from schemas import UserSchema, UserRegisterSchema, UserLoginSchema, TokenSchema
from flask_jwt_extended import get_jwt_identity

user_bp = Blueprint("users", __name__, description = "Make an account")

#user_schema = UserSchema()
#user_register_schema = UserRegisterSchema()
#user_login_schema = UserLoginSchema()
#token_schema = TokenSchema()

# 🟢 REGISTER
# 🟢 REGISTER
@user_bp.route("/register")
class UserRegister(MethodView):

    @user_bp.arguments(UserRegisterSchema)
    @user_bp.response(201, UserSchema)
    def post(self, data):
        """Register a new user"""

        if User.query.filter_by(username=data["username"]).first():
            abort(409, message="User already exists")

        user = User(username=data["username"])
        user.set_password(data["password"])

        db.session.add(user)
        db.session.commit()

        return user



# 🔐 LOGIN
@user_bp.route("/login")
class UserLogin(MethodView):

    @user_bp.arguments(UserLoginSchema)
    @user_bp.response(200, TokenSchema)
    def post(self, data):
        """Login user"""

        user = User.query.filter_by(username=data["username"]).first()
        if not user or not user.check_password(data["password"]):
            abort(401, message="Invalid credentials")

        access_token = create_access_token(identity=str(user.id))
        return {"access_token": access_token}



# ==================== LOGOUT ====================
@user_bp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    @user_bp.doc(security=[{"bearerAuth": []}])  # Shows lock icon in Swagger
    @user_bp.response(200, description="Logout successful (client should delete token)")
    def post(self):
        """Logout - client should delete the stored token"""
        return {"message": "Logged out successfully. Please delete your access token."}, 200


@user_bp.route("/")
class UserList(MethodView):
    @jwt_required()
    @user_bp.doc(security=[{"bearerAuth": []}])  # Shows lock icon in Swagger
    @user_bp.response(200, UserSchema(many=True))
    @user_bp.arguments(Schema, location='query')  # ← THIS IS THE FIX
    def get(self, query_args=None):  # You can ignore the argument
        """Get list of all users (protected endpoint - for testing/admin)"""
        users = User.query.all()
        return users