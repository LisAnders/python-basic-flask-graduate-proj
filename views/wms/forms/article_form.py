from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, FloatField
from wtforms.validators import DataRequired, Length


class ArticleForm(FlaskForm):
    code = StringField(
        label='Код товара:',
        validators=[DataRequired(), Length(min=3, max=10)],
        id='artCode',
        render_kw={'placeholder': 'Код товара'},
    )
    name = StringField(
        label='Наименование:',
        validators=[DataRequired(), Length(max=100)],
        render_kw={'placeholder': 'Наименование товара'},
    )
    is_online = BooleanField(
        label='Для онлайн продаж:',
    )
    
    price_buy = FloatField(
        label='Цена закупки:',
        validators=[DataRequired()],
        render_kw={'placeholder': 'Цена закупки'},
    )
    
    price_sale = FloatField(
        label='Цена продажи:',
        validators=[DataRequired()],
        render_kw={'placeholder': 'Цена продажи'},
    )
    
   