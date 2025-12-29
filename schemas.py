from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.adhkar import Adhkar
from models.favorite_adhkar import FavoriteAdhkar
from models.ahadith_ramadhania import AhadithRamadhania
from models.doua import Doua
from models.favorite_doua import FavoriteDoua

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

class RecipeCreateSchema(Schema):
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    ingredients = fields.List(fields.Dict(), required=True)
    steps = fields.Str(required=True)


class RecipeSchema(RecipeCreateSchema):
    id = fields.Int(dump_only=True)
    nutrition_summary = fields.Dict(dump_only=True)
    diabetic_friendly = fields.Bool(dump_only=True)
    pcos_friendly = fields.Bool(dump_only=True)
    pcos_score = fields.Int(dump_only=True)
    created_by_user_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

class UserAdhkarSchema(Schema):
    id = fields.Int(dump_only=True)
    text_ar = fields.Str(required=True)
    text_latin = fields.Str()
    category = fields.Str()
    created_at = fields.DateTime(dump_only=True)

class UserDouaSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    text_ar = fields.Str(required=True)
    text_latin = fields.Str()
    category = fields.Str()
    created_at = fields.DateTime(dump_only=True)

class KhatmaSchema(Schema):
    id = fields.Int(dump_only=True)
    unit = fields.Str(required=True)
    total_completed = fields.Int(dump_only=True)
    current_progress = fields.Int()
    status = fields.Str(dump_only=True)
    completion_date = fields.Date(dump_only=True)
    completion_doua = fields.Str(dump_only=True)

class SunnahPrayerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    is_ramadhan_only = fields.Bool()

class FavoriteAdhkarSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FavoriteAdhkar
        load_instance = True


class FavoriteDouaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FavoriteDoua
        load_instance = True
        include_fk = True  # include doua_id and user_id

class FavoriteRecipeSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    recipe_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
