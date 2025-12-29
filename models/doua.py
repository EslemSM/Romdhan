from .db import db

class Doua(db.Model):
    __tablename__ = "doua"

    id = db.Column(db.Integer, primary_key=True)
    allah_name = db.Column(db.String(100))
    text_ar = db.Column(db.Text, nullable=False)
    text_latin = db.Column(db.Text)
    name_latin = db.Column(db.String(100))
