from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin,db.Model):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(80),nullable=False,unique=True)
	email = db.Column(db.String(120),nullable=False,unique=True)
	password = db.Column(db.String(120),nullable=False,unique=True)
	
	def toDict(self):
		return{
		"id":self.id,
		"username":self.username,
		"email":self.email,
		"password":self.password
		}

	def set_password(self,password):
		self.password = generate_password_hash(password, method='sha256')

	def check_password(self,password):
		return check_password_hash(self.password,password)

class Topic(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	Title = db.Column(db.String(80),nullable=True)
	content = content = db.Column(db.Text,nullable=True)


class Post(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	content = db.Column(db.Text,nullable=True)
	topic = db.Column(db.String(80),nullable=True)
	rating = db.Column(db.Integer)
	author = db.Column(db.String(80),nullable=True)
	
	def toDict(self): 
		return{
		"id":self.id,
		"content":self.content,
		}
		
class Activity(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(80),nullable=True)
	type = db.Column(db.String(80),nullable=True)
	topic = db.Column(db.String(80),nullable = True)

class Workout(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(80),nullable=True)
	author = db.Column(db.String(80),nullable=True)
	E1 = db.Column(db.Integer,nullable=True)
	E2 = db.Column(db.Integer,nullable=True)
	E3 = db.Column(db.Integer,nullable=True)
	E4 = db.Column(db.Integer,nullable=True)
	E5 = db.Column(db.Integer,nullable=True)
	R1 = db.Column(db.Integer,nullable=True)
	R2 = db.Column(db.Integer,nullable=True)
	R3 = db.Column(db.Integer,nullable=True)
	R4 = db.Column(db.Integer,nullable=True)
	R5 = db.Column(db.Integer,nullable=True)
	S1 = db.Column(db.Integer,nullable=True)
	S2 = db.Column(db.Integer,nullable=True)
	S3 = db.Column(db.Integer,nullable=True)
	S4 = db.Column(db.Integer,nullable=True)
	S5 = db.Column(db.Integer,nullable=True)

	def toDict(self):
		return{
		"id":self.id,
		"content":self.content,
		}
	

