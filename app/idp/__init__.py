from flask import Blueprint
from app.idp.crud import get_user_institution

# Blueprint for the Identity Provider
bp = Blueprint('idp', __name__)
from app.idp import routes


