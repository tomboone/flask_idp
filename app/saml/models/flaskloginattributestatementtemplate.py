from flask_login import current_user
from flask_saml2.idp.xml_templates import AttributeStatementTemplate, AttributeTemplate
from app.saml.crud import saml_get_user_institution


# AttributeStatementTemplate subclass for Flask-Login
class FlaskLoginAttributeStatementTemplate(AttributeStatementTemplate):

    # generate_xml method
    def generate_xml(self):
        attributes = self.params.get('ATTRIBUTES', {  # Release additional attributes
            'uid': current_user.username,  # Username
            'mail': current_user.email,  # Email
            'sn': current_user.last_name,  # Last name
            'givenName': current_user.first_name,  # First name
            'eduPersonAffiliation': saml_get_user_institution(current_user).name,  # Institution
        })
        if not attributes:  # If there are no attributes
            return None  # Return None

        # Return the AttributeStatement XML
        return self.element('AttributeStatement', children=[
            AttributeTemplate({'ATTRIBUTE_NAME': name, 'ATTRIBUTE_VALUE': value}).xml
            for name, value in attributes.items()  # For each attribute, return the Attribute XML
        ])
