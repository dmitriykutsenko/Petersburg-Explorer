from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired


class EmailVerificationForm(FlaskForm):
    code = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Подтвердить регистрацию')
