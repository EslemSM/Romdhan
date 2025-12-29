from flask import Blueprint
from models.ahadith_ramadhania import AhadithRamadhania
from schemas import AhadithRamadhaniaSchema

ahadith_bp = Blueprint('ahadith', __name__)

schema = AhadithRamadhaniaSchema()
list_schema = AhadithRamadhaniaSchema(many=True)


@ahadith_bp.route('/', methods=['GET'])
def get_all():
    return list_schema.dump(AhadithRamadhania.query.all()), 200


@ahadith_bp.route('/<string:category>', methods=['GET'])
def get_by_category(category):
    hadith = AhadithRamadhania.query.filter_by(category=category).all()
    return list_schema.dump(hadith), 200
