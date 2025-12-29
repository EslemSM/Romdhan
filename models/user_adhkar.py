from .db import db
from datetime import datetime, timezone

class UserAdhkar(db.Model):
    __tablename__ = "user_adhkar"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    text_ar = db.Column(db.Text, nullable=False)
    text_latin = db.Column(db.Text)
    category = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
