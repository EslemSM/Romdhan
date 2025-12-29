from flask import Blueprint, request
from models.recipe import Recipe
from models.db import db
from schemas import RecipeSchema

recipe_bp = Blueprint('recipes', __name__)

schema = RecipeSchema()
list_schema = RecipeSchema(many=True)


@recipe_bp.route('/', methods=['GET'])
def get_all():
    return list_schema.dump(Recipe.query.all()), 200


@recipe_bp.route('/category/<string:category>', methods=['GET'])
def get_by_category(category):
    return list_schema.dump(Recipe.query.filter_by(category=category).all()), 200


@recipe_bp.route('/', methods=['POST'])
def add_recipe():
    recipe = Recipe(**request.get_json())
    recipe.diabetic_friendly = True
    recipe.pcos_friendly = True
    recipe.pcos_score = 85
    db.session.add(recipe)
    db.session.commit()
    return schema.dump(recipe), 201
