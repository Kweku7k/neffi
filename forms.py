from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    course = StringField('Course', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class Questions(FlaskForm):
    question = StringField('Phone', validators=[DataRequired()])
    q_number = StringField('Question Number')
    skillGroup = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Submit')


    