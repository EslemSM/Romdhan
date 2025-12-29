from .db import db

class AhadithRamadhania(db.Model):
    __tablename__ = "ahadith_ramadhania"

    id = db.Column(db.Integer, primary_key=True)
    text_ar = db.Column(db.Text, nullable=False)
    meaning_en = db.Column(db.Text)
    reference = db.Column(db.Text)
    category = db.Column(db.Text)
