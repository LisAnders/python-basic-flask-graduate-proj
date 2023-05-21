from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class WsForm(FlaskForm):
    name = StringField(
        label='Название МХ',
        validators=[DataRequired()],
        render_kw={'placeholder': 'Input warehouse name'},
        
    )
    