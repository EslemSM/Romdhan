from .db import db

class SunnahPrayer(db.Model):
    __tablename__ = "sunnah_prayer"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.Enum("duha", "taraweeh", "tahajjud"),
        nullable=False
    )
    is_ramadhan_only = db.Column(db.Boolean, default=False)
