from .db import db
from datetime import datetime, timezone
from passlib.hash import pbkdf2_sha256  # Ensure this is pbkdf2_sha256

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # 🔐 Helpers
    def set_password(self, password):
        if not password:
            raise ValueError("Password is required")
        # pbkdf2_sha256 allows unlimited length
        self.password_hash = pbkdf2_sha256.hash(password)

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password_hash) if self.password_hash else False