from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.recipe import Recipe
from models.favorite_recipe import FavoriteRecipe
from models.db import db
from schemas import RecipeSchema, RecipeCreateSchema, FavoriteRecipeSchema

recipe_bp = Blueprint('recipes', __name__)

create_schema = RecipeCreateSchema()
schema = RecipeSchema()
list_schema = RecipeSchema(many=True)
favorite_schema = FavoriteRecipeSchema()

# ✅ GET all public recipes
@recipe_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_public():
    recipes = Recipe.query.filter_by(created_by_user_id=None).all()
    return list_schema.dump(recipes), 200

# ✅ GET public recipes by taste
@recipe_bp.route('/taste/<string:taste>', methods=['GET'])
@jwt_required()
def get_public_by_taste(taste):
    if taste not in ['sweet', 'savory']:
        return {"error": "Invalid taste. Must be 'sweet' or 'savory'."}, 400
    recipes = Recipe.query.filter_by(taste=taste, created_by_user_id=None).all()
    return list_schema.dump(recipes), 200

# ✅ GET public recipes by category
@recipe_bp.route('/category/<string:category>', methods=['GET'])
@jwt_required()
def get_public_by_category(category):
    if category not in ['traditional', 'pcos_friendly']:
        return {"error": "Invalid category. Must be 'traditional' or 'pcos_friendly'."}, 400
    recipes = Recipe.query.filter_by(category=category, created_by_user_id=None).all()
    return list_schema.dump(recipes), 200

# ✅ GET user's own recipes
@recipe_bp.route('/my-recipes', methods=['GET'])
@jwt_required()
def get_my_recipes():
    user_id = get_jwt_identity()
    recipes = Recipe.query.filter_by(created_by_user_id=user_id).all()
    return list_schema.dump(recipes), 200

# ✅ GET user's own recipes by taste
@recipe_bp.route('/my-recipes/taste/<string:taste>', methods=['GET'])
@jwt_required()
def get_my_recipes_by_taste(taste):
    if taste not in ['sweet', 'savory']:
        return {"error": "Invalid taste. Must be 'sweet' or 'savory'."}, 400
    user_id = get_jwt_identity()
    recipes = Recipe.query.filter_by(created_by_user_id=user_id, taste=taste).all()
    return list_schema.dump(recipes), 200

# ✅ GET user's own recipes by category
@recipe_bp.route('/my-recipes/category/<string:category>', methods=['GET'])
@jwt_required()
def get_my_recipes_by_category(category):
    if category not in ['traditional', 'pcos_friendly']:
        return {"error": "Invalid category. Must be 'traditional' or 'pcos_friendly'."}, 400
    user_id = get_jwt_identity()
    recipes = Recipe.query.filter_by(created_by_user_id=user_id, category=category).all()
    return list_schema.dump(recipes), 200

# ✅ POST add user recipe
@recipe_bp.route('/', methods=['POST'])
@jwt_required()
def add_recipe():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate enums
    if data.get('taste') not in ['sweet', 'savory']:
        return {"error": "Invalid taste. Must be 'sweet' or 'savory'."}, 400
    if data.get('category') not in ['traditional', 'pcos_friendly']:
        return {"error": "Invalid category. Must be 'traditional' or 'pcos_friendly'."}, 400
    
    recipe = Recipe(**data)
    recipe.created_by_user_id = user_id
    db.session.add(recipe)
    db.session.commit()
    return schema.dump(recipe), 201

# ✅ GET user's favorites (full recipe details)
@recipe_bp.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    user_id = get_jwt_identity()
    favorites = FavoriteRecipe.query.filter_by(user_id=user_id).all()
    result = []
    for fav in favorites:
        recipe = Recipe.query.get(fav.recipe_id)
        if recipe:
            result.append(schema.dump(recipe))
    return result, 200

# ✅ POST add to favorites
@recipe_bp.route('/favorites', methods=['POST'])
@jwt_required()
def add_favorite():
    user_id = get_jwt_identity()
    data = request.get_json()
    recipe_id = data.get("recipe_id")
    if not recipe_id:
        return {"error": "recipe_id is required"}, 400
    
    # Ensure recipe exists and is accessible (public or own)
    recipe = Recipe.query.filter(
        (Recipe.id == recipe_id) & ((Recipe.created_by_user_id == user_id) | (Recipe.created_by_user_id == None))
    ).first()
    if not recipe:
        return {"error": "Recipe not found or not accessible"}, 404
    
    existing = FavoriteRecipe.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if existing:
        return {"error": "Already in favorites"}, 400
    
    favorite = FavoriteRecipe(user_id=user_id, recipe_id=recipe_id)
    db.session.add(favorite)
    db.session.commit()
    return {"message": "Added to favorites"}, 201

# ✅ DELETE remove from favorites
@recipe_bp.route('/favorites/<int:recipe_id>', methods=['DELETE'])
@jwt_required()
def remove_favorite(recipe_id):
    user_id = get_jwt_identity()
    favorite = FavoriteRecipe.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if not favorite:
        return {"error": "Favorite not found"}, 404
    db.session.delete(favorite)
    db.session.commit()
    return {"message": "Removed from favorites"}, 200

# ... (rest of the file remains unchanged)

# ✅ PATCH update a user's own recipe
@recipe_bp.route('/my-recipes/<int:id>', methods=['PATCH'])
@jwt_required()
def update_my_recipe(id):
    user_id = get_jwt_identity()
    recipe = Recipe.query.filter_by(id=id, created_by_user_id=user_id).first_or_404()
    
    data = request.get_json()
    # Validate enums if provided
    if 'taste' in data and data['taste'] not in ['sweet', 'savory']:
        return {"error": "Invalid taste. Must be 'sweet' or 'savory'."}, 400
    if 'category' in data and data['category'] not in ['traditional', 'pcos_friendly']:
        return {"error": "Invalid category. Must be 'traditional' or 'pcos_friendly'."}, 400
    
    # Update allowed fields
    for key, value in data.items():
        if hasattr(recipe, key) and key not in ['id', 'created_by_user_id', 'created_at']:
            setattr(recipe, key, value)
    
    db.session.commit()
    return schema.dump(recipe), 200

# ✅ DELETE a user's own recipe
@recipe_bp.route('/my-recipes/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_my_recipe(id):
    user_id = get_jwt_identity()
    recipe = Recipe.query.filter_by(id=id, created_by_user_id=user_id).first_or_404()
    
    db.session.delete(recipe)
    db.session.commit()
    return {"message": "Recipe deleted"}, 200

# ... (rest of the file remains unchanged)