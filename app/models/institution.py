from app.extensions import db


class Institution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime())
    updated = db.Column(db.DateTime())

    def __repr__(self):
        return f"<Institution {self.name}>"
