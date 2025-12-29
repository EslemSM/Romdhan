from .db import db
from datetime import datetime, timezone

class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.Enum("sweet", "savory"), nullable=False)

    ingredients = db.Column(db.JSON, nullable=False)
    steps = db.Column(db.Text, nullable=False)

    nutrition_summary = db.Column(db.JSON)
    diabetic_friendly = db.Column(db.Boolean)
    pcos_friendly = db.Column(db.Boolean)
    pcos_score = db.Column(db.Integer)

    created_by_user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=True
    )

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
