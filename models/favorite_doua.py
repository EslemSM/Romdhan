from .db import db
from datetime import datetime, timezone

class FavoriteDoua(db.Model):
    __tablename__ = "favorite_doua"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    doua_id = db.Column(db.Integer, db.ForeignKey("doua.id"), nullable=False)
    doua = db.relationship("Doua", backref="favorites")  # relationship to Doua
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
