from .db import db
from datetime import datetime, timezone

class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    taste = db.Column(db.Enum("sweet", "savory"), nullable=False)  # New: sweet/savory
    ingredients = db.Column(db.JSON, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    created_by_user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=True
    )
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    category = db.Column(db.Enum("traditional", "pcos_friendly"), nullable=False)  # Updated: traditional/pcos_friendly
	