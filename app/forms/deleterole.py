from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class DeleteRoleForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
