from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField
from wtforms.validators import InputRequired, EqualTo
from wtforms.fields.html5 import EmailField

class SignUp(FlaskForm):
    username = StringField('Username', validators=[InputRequired()],render_kw={'class': 'white-text'})
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Enter Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Confirm Password')
    submit = SubmitField('Create Account', render_kw={'class': 'btn black-text red accent-4'})

class Login(FlaskForm):
    username = StringField('Username', validators=[InputRequired()],render_kw={'class': 'white-text'})
    password = PasswordField('Enter Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match')])
    submit = SubmitField('Login', render_kw={'class': 'btn black-text red accent-4'})

class NewTopic(FlaskForm):
	title = StringField('Title', validators=[InputRequired()],render_kw={'class': 'white-text'})
	content =TextAreaField('New Post....',validators =[InputRequired()])
	submit = SubmitField('Publish', render_kw={'class': 'btn black-text red accent-4'})

class NewPost(FlaskForm):
	content =TextAreaField('New Post....',validators =[InputRequired()])
	submit = SubmitField('Post', render_kw={'class': 'btn black-text red accent-4'})
	topic = StringField()


class NewWorkout(FlaskForm):
	Title = StringField('Workout Name')
	Excercise1 = StringField('Excercise')
	Excercise2 = StringField('Excercise')
	Excercise3 = StringField('Excercise')
	Excercise4 = StringField('Excercise')
	Excercise5 = StringField('Excercise')
	Reps1 = StringField('Reps')
	Reps2 = StringField('Reps')
	Reps3 = StringField('Reps')
	Reps4 = StringField('Reps')
	Reps5 = StringField('Reps')
	Sets1 = StringField('Sets')
	Sets2 = StringField('Sets')
	Sets3 = StringField('Sets')
	Sets4 = StringField('Sets')
	Sets5 = StringField('Sets')
	submit = SubmitField('Create', render_kw={'class': 'btn black-text red accent-4'})
	

