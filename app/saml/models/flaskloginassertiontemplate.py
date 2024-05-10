from flask_saml2.idp.xml_templates import AssertionTemplate
from flask_saml2.types import XmlNode
from app.saml.models.flaskloginattributestatementtemplate import FlaskLoginAttributeStatementTemplate


# AssertionTemplate subclass for Flask-Login
class FlaskLoginAssertionTemplate(AssertionTemplate):

    # _get_attribute_statement method
    def _get_attribute_statement(self) -> XmlNode:
        return FlaskLoginAttributeStatementTemplate(self.params).xml  # Return the AttributeStatement XML
