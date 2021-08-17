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
    component= SelectField('Component', choices=[('--Component--', '--Component--'),('Prior Knowledge', 'Prior Knowledge'), ('Social Engagement', 'Social Engagement'), ('Relevance', 'Relevance'), ('Application', 'Application'),('Lecture Focus', 'Lecture Focus'),('Meaningful Application', 'Meaningful Application'),('Organisation', 'Organisation'),('Visualization', 'Visualization'),('Elaboration', 'Elaboration'),('Repetition', 'Repetition'),('Empowerment', 'Empowerment'),('Usefulness', 'Usefulness'),('Success', 'Success'),('Interest', 'Interest'),('Caring', 'Caring')])
    skillGroup = SelectField('Skill Group', choices=[('--Skill Group--', '--Skill Group--'),('Learner Centricity', 'Learner Centricity'),('Teaching for Recall', 'Teaching for Recall'),('Teaching for Engagement', 'Teaching for Engagement')])
    submit = SubmitField('Submit')


    