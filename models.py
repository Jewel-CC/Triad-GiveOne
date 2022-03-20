from ctypes import addressof
import datetime

from flask_sqlalchemy import SQLAlchemy
from pytest import Item
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from flask_login import UserMixin


db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name =  db.Column(db.String, nullable=False)
    last_name =  db.Column(db.String, nullable=False)
    username =  db.Column(db.String(80), unique=True, nullable=False)
    bio =  db.Column(db.String(220), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), unique=True, nullable=False)
    dob = db.Column(db.Date, unique=True, nullable=False)


    def toDict(self):
        return{
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'bio': self.bio,
            'password':self.password,
            'address':self.address,
            'dob':self.dob
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.email) 

class Giver(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    donation = relationship("Request", backref="Giver")


    def toDict(self):
        return{
            'id':self.id,
            'donation': self.donation
        }

class Getter(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    # ver_status = db.Column(db.bool, nullable=False)
    # requests = db.Column(relationship("Request", backref="Getter"))


    def toDict(self):
        return{
        'id':self.id,
        'ver_status': self.ver_status   
        }

class Request(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    status = db.Column(db.Boolean, nullable=False) #add default value
    description = db.Column(db.String, nullable=False) 
    item = relationship("Item", backref="Request")
    category = db.column(db.String(80))
    urgent = db.Column(db.Boolean, nullable=False)

    def toDict(self):
        return{
        'id':self.id,
        'title':self.title,
        'status': self.status,
        'description': self.description, 
        'item': self.item,
        'category': self.category,
        'urgent':self.urgent   
        }
    
class Item(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer) 
    


    def toDict(self):
        return{
        'id':self.id,
        'name':self.name,
        'quantity':self.quantity
        }
	
