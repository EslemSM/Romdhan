from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.adhkar import Adhkar
from models.favorite_adhkar import FavoriteAdhkar
from models.ahadith_ramadhania import AhadithRamadhania
from models.doua import Doua
from models.favorite_doua import FavoriteDoua
from models.khatma import Khatma
from models.recipe import Recipe
from models.favorite_recipe import FavoriteRecipe
from models.user_doua import UserDoua
from models.user_adhkar import UserAdhkar

class UserRegisterSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    created_at = fields.DateTime(dump_only=True)

class TokenSchema(Schema):
    access_token = fields.Str()

class AdhkarSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Adhkar
        load_instance = True
        include_fk = True


class DouaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Doua
        load_instance = True
        
class AhadithRamadhaniaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AhadithRamadhania
        load_instance = True

class RecipeCreateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Recipe
        load_instance = True
        exclude = ('id', 'created_by_user_id', 'created_at')  # Exclude auto-fields for creation

class RecipeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Recipe
        load_instance = True

class UserAdhkarSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserAdhkar
        load_instance = True
        include_fk = True

    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

class UserDouaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserDoua
        load_instance = True
        include_fk = True

    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

class KhatmaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Khatma
        load_instance = True
    unit = fields.Str(required=True)

class SunnahPrayerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    is_ramadhan_only = fields.Bool()

class FavoriteAdhkarSchema(SQLAlchemyAutoSchema):
    adhkar = fields.Nested(AdhkarSchema)

    class Meta:
        model = FavoriteAdhkar
        load_instance = True
        include_fk = True

class FavoriteDouaSchema(SQLAlchemyAutoSchema):
    doua = fields.Nested(DouaSchema)

    class Meta:
        model = FavoriteDoua
        load_instance = True
        include_fk = True

class FavoriteRecipeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FavoriteRecipe
        load_instance = True
