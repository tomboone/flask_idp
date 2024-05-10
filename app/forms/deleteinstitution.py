from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class DeleteInstitutionForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
