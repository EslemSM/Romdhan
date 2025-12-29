from flask import Blueprint, request
from models.khatma import Khatma
from models.db import db
from schemas import KhatmaSchema

khatma_bp = Blueprint('khatma', __name__)

schema = KhatmaSchema()
list_schema = KhatmaSchema(many=True)


@khatma_bp.route('/', methods=['GET'])
def get_current():
    return list_schema.dump(Khatma.query.all()), 200


@khatma_bp.route('/', methods=['POST'])
def add_session():
    khatma = Khatma(**request.get_json())
    db.session.add(khatma)
    db.session.commit()
    return schema.dump(khatma), 201


@khatma_bp.route('/<int:id>', methods=['PATCH'])
def update_progress(id):
    khatma = Khatma.query.get_or_404(id)
    data = request.get_json()
    khatma.current_progress += data.get("add", 0)
    db.session.commit()
    return schema.dump(khatma), 200


@khatma_bp.route('/<int:id>', methods=['DELETE'])
def delete_session(id):
    khatma = Khatma.query.get_or_404(id)
    db.session.delete(khatma)
    db.session.commit()
    return {"message": "Deleted"}, 200
