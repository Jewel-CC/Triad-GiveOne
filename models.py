from ctypes import addressof
import datetime

from flask_sqlalchemy import SQLAlchemy
from pytest import Item
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from uploads import store_file, remove_file


db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    # documents = db.Column(db.String(120), nullable=False)   #documents uploaded by user
    requests = db.relationship('Requests', backref='user', lazy=True, cascade="all, delete-orphan")     #get all requests by user
    donations = db.relationship('Donations', backref='user', lazy=True, cascade="all, delete-orphan")   #get all donations for user

    def toDict(self):
      return {
        "id": self.id,
        "username": self.username,
        "email": self.email,
        "password": self.password,
        "num_requests": self.getNumRequests(),
        "num_donations": self.getNumDonations()
      }

    def getNumRequests(self):
      return len(self.requests)

    def getNumDonations(self):
      return len(self.donations)

    #hashes the password parameter and stores it in the object
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    #Returns true if the parameter is equal to the object’s password property
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    #To String method
    def __repr__(self):
        return '<User {}>'.format(self.username)




class Requests(db.Model):
    reqid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)    
    body = db.Column(db.String(1000), nullable=False)
    # req_items = db.relationship('RequestItems', backref='requests', lazy=True, cascade="all, delete-orphan")     #get all requested items
    req_items = db.Column(db.String(2000), nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    donated = db.Column(db.Boolean, default=False)  
    directions = db.Column(db.String(1000), nullable=False, default="")
    note = db.Column(db.String(1000), nullable=False, default="")
    donator_username = db.Column(db.String(180), nullable=False, default="")
    donator_email =  db.Column(db.String(180), nullable=False, default="")

    def toDict(self):
        return {
            "reqid" : self.reqid,
            "title" : self.title,
            "body" : self.body,
            "items" : self.items,
            "userid" : self.userid
        }

# class RequestItems(db.Model):
#   itemid = db.Column(db.Integer, primary_key=True)
#   item_name = db.Column(db.String(100), nullable=False)
#   reqid = db.Column(db.Integer, db.ForeignKey('requests.reqid'), nullable=False)


class Donations(db.Model):
    donid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)    
    body = db.Column(db.String(1000), nullable=False)
    # don_items = db.relationship('DonationItems', backref='donations', lazy=True, cascade="all, delete-orphan")     #get all requests by user
    don_items = db.Column(db.String(2000), nullable=False)
    directions = db.Column(db.String(1000), nullable=False)
    note = db.Column(db.String(1000), nullable=False)
    userid  = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    requested = db.Column(db.Boolean, default=False)  
    requestor_username = db.Column(db.String(180), nullable=False, default="")
    requestor_email =  db.Column(db.String(180), nullable=False, default="")
    
    def toDict(self):
        return {
            "donid" : self.donid,
            "title" : self.title,
            "body" : self.body,
            "items" : self.items,
            "directions" : self.directions,
            "note" : self.note,
            "userid" : self.userid
        }

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, nullable=False)

    def __init__(self, file):
      self.filename = store_file(file)

    def remove_file(self):
      remove_file(self.filename)

    def get_url(self):
      return f'/uploads/{self.filename}'

        
# from ctypes import addressof
# import datetime

# from flask_sqlalchemy import SQLAlchemy
# from pytest import Item
# from werkzeug.security import generate_password_hash, check_password_hash
# from sqlalchemy.orm import relationship
# from flask_login import UserMixin


# db = SQLAlchemy()


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name =  db.Column(db.String, nullable=False)
#     last_name =  db.Column(db.String, nullable=False)
#     username =  db.Column(db.String(80), unique=True, nullable=False)
#     bio =  db.Column(db.String(220), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)
#     address = db.Column(db.String(120), unique=True, nullable=False)
#     dob = db.Column(db.Date, unique=True, nullable=False)


#     def toDict(self):
#         return{
#             'id': self.id,
#             'first_name': self.first_name,
#             'last_name': self.last_name,
#             'username': self.username,
#             'email': self.email,
#             'bio': self.bio,
#             'password':self.password,
#             'address':self.address,
#             'dob':self.dob
#         }

#     def set_password(self, password):
#         """Create hashed password."""
#         self.password = generate_password_hash(password, method='sha256')
    
#     def check_password(self, password):
#         """Check hashed password."""
#         return check_password_hash(self.password, password)
    
#     def __repr__(self):
#         return '<User {}>'.format(self.email) 

# class Giver(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     donation = relationship("Request", backref="Giver")


#     def toDict(self):
#         return{
#             'id':self.id,
#             'donation': self.donation
#         }

# class Getter(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     # ver_status = db.Column(db.bool, nullable=False)
#     # requests = db.Column(relationship("Request", backref="Getter"))


#     def toDict(self):
#         return{
#         'id':self.id,
#         'ver_status': self.ver_status   
#         }

# class Request(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     title = db.Column(db.String(120), nullable=False)
#     status = db.Column(db.Boolean, nullable=False) #add default value
#     description = db.Column(db.String, nullable=False) 
#     item = relationship("Item", backref="Request")
#     category = db.Column(db.String(80))
#     urgent = db.Column(db.Boolean, nullable=False)

#     def toDict(self):
#         return{
#         'id':self.id,
#         'title':self.title,
#         'status': self.status,
#         'description': self.description, 
#         'item': self.item,
#         'category': self.category,
#         'urgent':self.urgent   
#         }
    
# class Item(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     quantity = db.Column(db.Integer) 
    


#     def toDict(self):
#         return{
#         'id':self.id,
#         'name':self.name,
#         'quantity':self.quantity
#         }
	
