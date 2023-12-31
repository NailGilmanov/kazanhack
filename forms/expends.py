from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, TimeField
from wtforms.validators import DataRequired


class ExpendsForm(FlaskForm):
    category = StringField('Категория', validators=[DataRequired()])
    date = DateField("Дата покупки", format="'%d-%m-%Y'")
    price = SubmitField('Сумма', validators=[DataRequired()])
