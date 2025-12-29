from .db import db
from datetime import datetime, timezone

class UserDoua(db.Model):
    __tablename__ = "user_doua"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    title = db.Column(db.String(150))
    text_ar = db.Column(db.Text, nullable=False)
    text_latin = db.Column(db.Text)
    category = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
