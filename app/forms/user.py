from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag='ul', prefix_label=False)
    option_widget = widgets.CheckboxInput()


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    institution = SelectField('Institution', coerce=int)
