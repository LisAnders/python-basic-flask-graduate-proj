from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, FloatField
from wtforms.validators import DataRequired, Length

class OperationForm(FlaskForm):
    
    
    opnumber = StringField(
        label='Номер операции',
        validators=[DataRequired(), Length(max=20)],
        id = 'opNum',
        render_kw={'placeholder': 'Номер операции'},
    )
    
    opdate = DateField(
        label='Дата операции',
        validators=[DataRequired()],
        id='opDate',
        render_kw={'placeholder': 'Дата операции'},
    )
    
    wso = SelectField(
        label='МХ Откуда',
        validators=[DataRequired()],
    )
    
    wsi = SelectField(
        label='МХ Куда',
        validators=[DataRequired()],
    )
    
    status = SelectField(
        label='Статус',
        validators=[DataRequired()],
    )


class OpartForm(FlaskForm):
    
    id_art = SelectField(
        label='Товарная позиция',
    )
    
    quantity = FloatField(
        label='Количество',
        validators=[DataRequired()]
    )
    price = FloatField(
        label='Цена',
        validators=[DataRequired()]
    )