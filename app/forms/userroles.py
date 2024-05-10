from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, widgets


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class UserRolesForm(FlaskForm):
    roles = MultiCheckboxField('Roles')
