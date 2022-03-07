from html.entities import html5
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField, SelectField, RadioField, EmailField, validators, ValidationError
from wtforms.validators import InputRequired, EqualTo, Email



class SignUp(FlaskForm):
    username = StringField('Username', validators=[InputRequired()],render_kw={'class': 'white-text'})
    # email = EmailField('Email', validators=[Email(),InputRequired()])
    password = PasswordField('Enter Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords do not match')])
    confirm  = PasswordField('Confirm Password')
    submit = SubmitField('Create Account', render_kw={'class': 'btn black-text red accent-4'})

class Login(FlaskForm):
    username = StringField('Username', validators=[InputRequired()],render_kw={'class': 'white-text'})
    password = PasswordField('Enter Password', validators=[InputRequired()])
    submit = SubmitField('Login', render_kw={'class': 'btn black-text red accent-4'})

class newRequest(FlaskForm): 
    title = StringField('Title', validators=[InputRequired()],render_kw={'class': 'white-text'})
    desription =TextAreaField('Your request in 200 characters or less....',validators =[InputRequired()])
    category  = SelectField('Please choose the most appropriate tags to help identify your request', choices=[('Food'), ('School'), ('Medicine'), ('Furniture'), ('Clothing'), ('Custom')])
    item = StringField('Item', validators=[InputRequired()]) #List
    urgent = RadioField('Is this request urgent?', choices=[('No'), ('Yes')])
    submit = SubmitField('Publish', render_kw={'class': 'btn black-text red accent-4'})

class newDonation(FlaskForm):
    items = SelectField('', choices=[('Food')])
  