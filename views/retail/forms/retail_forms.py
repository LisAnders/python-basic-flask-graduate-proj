from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, FloatField
from wtforms.validators import DataRequired, Length

class RetailOpartForm(FlaskForm):
    barcode = StringField(
        label='Штрих-код:',
        validators=[DataRequired()],
        id = 'barcode',
        render_kw={'placeholder': 'Введите штрих-код'},
    )