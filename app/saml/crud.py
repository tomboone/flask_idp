from app import db
from app.models.institution import Institution


# Get a user's institution
def saml_get_user_institution(user):
    institution = db.one_or_404(db.select(Institution).filter(Institution.id == user.institution))
    return institution
