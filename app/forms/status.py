from flask_wtf import FlaskForm
from wtforms import StringField


class UserStatusForm(FlaskForm):
    userid = StringField('User ID')
