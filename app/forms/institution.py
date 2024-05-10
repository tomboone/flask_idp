from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


# Add/Edit Institution Form
class InstitutionForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
