from flask_saml2.idp import SPHandler
from app.saml.models.flaskloginassertiontemplate import FlaskLoginAssertionTemplate


# SPHandler subclass for Flask-Login
class FlaskLoginSPHandler(SPHandler):
    assertion_template = FlaskLoginAssertionTemplate  # Use the FlaskLoginAssertionTemplate for the Assertion XML

    # get_subject method
    def get_subject(self):
        return self.idp.get_user_nameid(self.idp.get_current_user(), self.subject_format)  # Return the user's NameID
