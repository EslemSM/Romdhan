from models.db import db
from datetime import datetime, timezone

class FavoriteAdhkar(db.Model):
    __tablename__ = 'favorite_adhkar'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    adhkar_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
