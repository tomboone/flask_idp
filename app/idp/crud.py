from app import db
from app.models.user import User
from app.models.role import Role
from app.models.institution import Institution
from datetime import datetime

#########
# ROLES #
#########


# Read all roles
def read_roles():
    roles = db.session.execute(db.select(Role).order_by(Role.name)).scalars()
    return roles


# Update a role
def update_role(role_id, name, description):
    role = db.one_or_404(db.select(Role).filter(Role.id == role_id))
    role.name = name
    role.description = description
    db.session.commit()
    return role


################
# INSTITUTIONS #
################


# Read all institutions
def read_institutions():
    institutions = db.session.execute(db.select(Institution).order_by(Institution.name)).scalars()
    return institutions


# Create an institution
def create_institution(code, name):
    institution = Institution()
    institution.code = code
    institution.name = name
    institution.created = datetime.now()
    institution.updated = datetime.now()
    db.session.add(institution)
    db.session.commit()
    return institution


# Read an institution
def read_institution(institution_code):
    institution = db.one_or_404(db.select(Institution).filter(Institution.code == institution_code))
    return institution


# Update an institution
def update_institution(inst_id, code, name):
    institution = db.one_or_404(db.select(Institution).filter(Institution.id == inst_id))
    institution.code = code
    institution.name = name
    institution.updated = datetime.now()
    db.session.commit()
    return institution


# Delete an institution
def delete_institution(inst_id):
    institution = db.one_or_404(db.select(Institution).filter(Institution.id == inst_id))
    db.session.delete(institution)
    db.session.commit()


#########
# USERS #
#########


# Read all active users
def read_active_users():
    users = db.session.execute(db.select(User).filter_by(active=1).order_by(User.id)).scalars()
    return users


def read_inactive_users():
    users = db.session.execute(db.select(User).filter(User.active!=1).order_by(User.id)).scalars()
    return users


# Update a user
def update_user(user_id, username, email, first_name, last_name, institution):
    user = db.one_or_404(db.select(User).filter(User.id == user_id))
    user.username = username
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.institution = institution
    user.updated = datetime.now()
    db.session.commit()
    return user


# Update a user's password
def update_password(user_id, password):
    user = db.one_or_404(db.select(User).filter(User.id == user_id))
    user.password = password
    user.updated = datetime.now()
    db.session.commit()
    return user


# Update user updated time
def update_user_updated(user_id):
    user = db.one_or_404(db.select(User).filter(User.id == user_id))
    user.updated = datetime.now()
    db.session.commit()
    return user


# Get a user's institution
def get_user_institution(user):
    institution = db.one_or_404(db.select(Institution).filter(Institution.id == user.institution))
    return institution
