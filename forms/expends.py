from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, TimeField
from wtforms.validators import DataRequired


class ExpendsForm(FlaskForm):
    category = StringField('Категория', validators=[DataRequired()])
    # date_and_time = DateTimeField("Дата и время проведения мероприятия", validators=[])
    date = DateField("Дата покупки", format="'%d-%m-%Y'")
    price = SubmitField('Сумма', validators=[DataRequired()])
