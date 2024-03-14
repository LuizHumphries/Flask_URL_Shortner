from src.repository.database import db

class UrlShortned(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(255), nullable=False)
    short_url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime)
    expire_at = db.Column(db.DateTime)

    def as_dict(self):
        return {
            "id": self.id,
            "long_url": self.long_url,
            "short_url": self.short_url,
            "created_at": self.created_at,
            "expire_at": self.expire_at
        }