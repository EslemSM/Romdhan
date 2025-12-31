from .db import db
from datetime import datetime, timezone
class Khatma(db.Model):
    __tablename__ = "khatma"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    unit = db.Column(db.Enum("juz", "hizb"), nullable=False)
    total_completed = db.Column(db.Integer, default=0)
    current_progress = db.Column(db.Integer, default=0)

    status = db.Column(
        db.Enum("in_progress", "completed"),
        default="in_progress"
    )

    completion_date = db.Column(db.Date)