from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, TimeField
from wtforms.validators import DataRequired


class ArrivalsForm(FlaskForm):
    date = DateField("Дата покупки", format="'%d-%m-%Y'")
    price = SubmitField('Сумма', validators=[DataRequired()])
