from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField
from wtforms.validators import DataRequired
from wtforms_alchemy import QuerySelectMultipleField

class UserForm(FlaskForm):
    username = StringField(
        label='UserName',
        validators=[DataRequired()],
        render_kw={'placeholder': 'username'},
    )
    
    roles = QuerySelectMultipleField(
        label='Роли',
    )