from flask import url_for, request, abort, redirect
from flask_login import current_user, logout_user
from flask_saml2.idp import IdentityProvider


# IdentityProvider subclass for Flask-Login
class FlaskLoginIdentityProvider(IdentityProvider):

    # login_required method
    def login_required(self):
        if not current_user.is_authenticated:  # If the user is not authenticated
            nexturl = url_for('security.login', next=request.url)  # Get the next URL to login
            abort(redirect(nexturl))  # Redirect to the next URL

    # logout method
    def logout(self):
        logout_user()  # Logout the user

    # get_current_user method
    def get_current_user(self):
        return current_user  # Return the current user
