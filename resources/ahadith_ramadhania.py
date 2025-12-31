from flask_smorest import Blueprint
from flask.views import MethodView
from models.ahadith_ramadhania import AhadithRamadhania
from schemas import AhadithRamadhaniaSchema
from flask_smorest import abort

ahadith_bp = Blueprint(
    'ahadith',
    __name__,
    description="Ahadith Ramadhania (Ramadan-related Hadiths)"
)

list_schema = AhadithRamadhaniaSchema(many=True)


@ahadith_bp.route('/')
class AhadithList(MethodView):
    @ahadith_bp.response(200, AhadithRamadhaniaSchema(many=True))
    def get(self):
        """Get all Ramadan Ahadith"""
        return AhadithRamadhania.query.all()


@ahadith_bp.route('/<string:category>')
class AhadithByCategory(MethodView):
    @ahadith_bp.response(200, AhadithRamadhaniaSchema(many=True))
    @ahadith_bp.alt_response(404, description="Category not found")
    def get(self, category):
        """Get Ahadith by category"""
        hadiths = AhadithRamadhania.query.filter_by(category=category).all()
        if not hadiths:
            abort(404, message="No hadiths found for this category")
        return hadiths