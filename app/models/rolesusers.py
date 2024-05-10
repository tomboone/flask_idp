from app.extensions import db


class RolesUsers(db.Model):
    __table_args__ = {'extend_existing': True}
    user_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.ForeignKey('role.id'), primary_key=True)

    def __repr__(self):
        return f"<RolesUsers User: {self.user_id} + Role: {self.role_id}>"
