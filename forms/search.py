from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields import StringField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    searched = StringField('Поиск', validators=[DataRequired()])
    submit = SubmitField('Найти')
