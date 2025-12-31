from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields
from models.recipe import Recipe
from models.favorite_recipe import FavoriteRecipe
from models.db import db
from schemas import RecipeSchema

# -------------------------------------------------------------------
# Blueprint
# -------------------------------------------------------------------
recipe_bp = Blueprint(
    "recipes",
    __name__,
    description="Recipes & favorites management"
)

# -------------------------------------------------------------------
# Response schemas
# -------------------------------------------------------------------
recipe_schema = RecipeSchema()
recipe_list_schema = RecipeSchema(many=True)

# -------------------------------------------------------------------
# Input schemas (Swagger request bodies)
# -------------------------------------------------------------------
class RecipeCreateSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str()
    ingredients = fields.Str()
    steps = fields.Str()
    taste = fields.Str(required=True, validate=lambda x: x in ["sweet", "savory"])
    category = fields.Str(required=True, validate=lambda x: x in ["traditional", "pcos_friendly"])

class RecipePatchSchema(Schema):
    title = fields.Str()
    description = fields.Str()
    ingredients = fields.Str()
    steps = fields.Str()
    taste = fields.Str(validate=lambda x: x in ["sweet", "savory"])
    category = fields.Str(validate=lambda x: x in ["traditional", "pcos_friendly"])

class FavoriteRecipeCreateSchema(Schema):
    recipe_id = fields.Int(required=True)


# -------------------------------------------------------------------
# 🔐 GET all public recipes
# -------------------------------------------------------------------
@recipe_bp.route("/", methods=["GET"])
@recipe_bp.doc(security=[{"bearerAuth": []}])
@recipe_bp.response(200, recipe_list_schema)
@jwt_required()
def get_all_public():
    return Recipe.query.filter_by(created_by_user_id=None).all()


# -------------------------------------------------------------------
# 🔐 GET public recipes by taste
# -------------------------------------------------------------------
@recipe_bp.route("/taste/<string:taste>", methods=["GET"])
@recipe_bp.doc(security=[{"bearerAuth": []}])
@recipe_bp.response(200, recipe_list_schema)
@jwt_required()
def get_public_by_taste(taste):
    if taste not in ["sweet", "savory"]:
        return {"error": "Invalid taste"}, 400

    return Recipe.query.filter_by(
        taste=taste,
        created_by_user_id=None
    ).all()


# -------------------------------------------------------------------
# 🔐 GET public recipes by category
# -------------------------------------------------------------------
@recipe_bp.route("/category/<string:category>", methods=["GET"])
@recipe_bp.doc(security=[{"bearerAuth": []}])
@recipe_bp.response(200, recipe_list_schema)
@jwt_required()
def get_public_by_category(category):
    if category not in ["traditional", "pcos_friendly"]:
        return {"error": "Invalid category"}, 400

    return Recipe.query.filter_by(
        category=category,
        created_by_user_id=None
    ).all()


# -------------------------------------------------------------------
# 🔐 GET user's own recipes
# -------------------------------------------------------------------
@recipe_bp.route("/my-recipes", methods=["GET"])
@recipe_bp.doc(security=[{"bearerAuth": []}])
@recipe_bp.response(200, recipe_list_schema)
@jwt_required()
def get_my_recipes():
    user_id = get_jwt_identity()
    return Recipe.query.filter_by(created_by_user_id=user_id).all()


# -------------------------------------------------------------------
# 🔐 POST add recipe
# -------------------------------------------------------------------
@recipe_bp.route("/", methods=["POST"])
@recipe_bp.doc(security=[{"bearerAuth": []}])
@recipe_bp.arguments(RecipeCreateSchema)
@recipe_bp.response(201, recipe_schema)
@jwt_required()
def add_recipe(data):
    user_id = get_jwt_identity()

    recipe = Recipe(**data)
    recipe.created_by_user_id = user_id

    db.session.add(recipe)
    db.session.commit()
    return recipe


# -------------------------------------------------------------------
# 🔐 PATCH update user's recipe
# -------------------------------------------------------------------
@recipe_bp.route("/my-recipes/<int:id>", methods=["PATCH"])
@recipe_bp.doc(security=[{"bearerAuth": []}])
@recipe_bp.arguments(RecipePatchSchema)
@recipe_bp.response(200, recipe_schema)
@jwt_required()
def update_my_recipe(data, id):
    user_id = get_jwt_identity()

    recipe = Recipe.query.filter_by(
        id=id,
        created_by_user_id=user_id
    ).first_or_404()

    for key, value in data.items():
        setattr(recipe, key, value)

    db.session.commit()
    return recipe


# -------------------------------------------------------------------
# 🔐 DELETE user's recipe
# -------------------------------------------------------------------
@recipe_bp.route("/my-recipes/<int:id>", methods=["DELETE"])
@recipe_bp.doc(security=[{"bearerAuth": []}])
@recipe_bp.response(200)
@jwt_required()
def delete_my_recipe(id):
    user_id = get_jwt_identity()

    recipe = Recipe.query.filter_by(
        id=id,
        created_by_user_id=user_id
    ).first_or_404()

    db.session.delete(recipe)
    db.session.commit()
    return {"message": "Recipe deleted"}


# -------------------------------------------------------------------
# 🔐 GET favorites
# -------------------------------------------------------------------
@recipe_bp.route("/favorites", methods=["GET"])
@recipe_bp.doc(security=[{"bearerAuth": []}])
@recipe_bp.response(200, recipe_list_schema)
@jwt_required()
def get_favorites():
    user_id = get_jwt_identity()

    favorites = FavoriteRecipe.query.filter_by(user_id=user_id).all()
    recipes = []

    for fav in favorites:
        recipe = Recipe.query.get(fav.recipe_id)
        if recipe:
            recipes.append(recipe)

    return recipes

@recipe_bp.route("/favorites", methods=["POST"])
@recipe_bp.doc(security=[{"bearerAuth": []}])
@recipe_bp.arguments(FavoriteRecipeCreateSchema)
@recipe_bp.response(201)
@jwt_required()
def add_favorite(data):
    user_id = get_jwt_identity()
    recipe_id = data["recipe_id"]

    recipe = Recipe.query.filter(
        (Recipe.id == recipe_id)
        & ((Recipe.created_by_user_id == user_id) | (Recipe.created_by_user_id == None))
    ).first_or_404()

    existing = FavoriteRecipe.query.filter_by(
        user_id=user_id,
        recipe_id=recipe_id
    ).first()

    if existing:
        return {"error": "Already in favorites"}, 400

    favorite = FavoriteRecipe(user_id=user_id, recipe_id=recipe_id)
    db.session.add(favorite)
    db.session.commit()

    return {"message": "Added to favorites"}

@recipe_bp.route("/favorites/<int:recipe_id>", methods=["DELETE"])
@recipe_bp.doc(security=[{"bearerAuth": []}])
@recipe_bp.response(200)
@jwt_required()
def remove_favorite(recipe_id):
    user_id = get_jwt_identity()

    favorite = FavoriteRecipe.query.filter_by(
        user_id=user_id,
        recipe_id=recipe_id
    ).first_or_404()

    db.session.delete(favorite)
    db.session.commit()

    return {"message": "Removed from favorites"}
