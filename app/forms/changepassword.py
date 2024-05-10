from flask_wtf import FlaskForm
from wtforms import PasswordField, IntegerField
from wtforms.validators import DataRequired


class ChangePasswordForm(FlaskForm):
    user_id = IntegerField("User ID")
    new_password = PasswordField("New Password", validators=[DataRequired()])
