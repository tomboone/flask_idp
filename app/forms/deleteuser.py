from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class DeleteUserForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
