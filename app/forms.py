from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import BooleanField, FileField, PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(max=180)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=180)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=128)])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match.')],
    )
    submit = SubmitField('Create account')

    def validate_email(self, field):
        if not field.data.lower().endswith('@gmail.com'):
            raise ValidationError('Only @gmail.com email addresses are allowed.')


class ResumeUploadForm(FlaskForm):
    resume_file = FileField(
        'Upload resume',
        validators=[
            FileRequired(message='Resume file is required.'),
            FileAllowed(['pdf', 'docx'], 'Only PDF and DOCX files are supported.'),
        ],
    )
    job_description = StringField(
        'Job description',
        validators=[Length(max=5000)],
        description='Paste the target role description to compare your CV against it.',
    )
    submit = SubmitField('Upload Resume')
