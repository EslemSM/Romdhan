from .db import db

class Adhkar(db.Model):
    __tablename__ = "adhkar"

    id = db.Column(db.Integer, primary_key=True)
    text_ar = db.Column(db.Text, nullable=False)
    transliteration = db.Column(db.Text)
    category = db.Column(
        db.Enum(
            'morning','evening','night','going_out','going_in',
            'before_suhur','after_suhur','before_iftar','after_iftar'
        ),
        nullable=False
    )
    translation = db.Column(db.Text)
    count = db.Column(db.Integer)
    source = db.Column(db.Text)
