from flask import Flask, request, jsonify, render_template, redirect, flash, url_for, jsonify, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from datetime import timedelta
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
import os
import smtplib, datetime

from models import Donation_Image, db, User, Requests, Donations, Upload, Request_Image

''' Begin Flask Login Functions '''
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

''' End Flask Login Functions '''

''' Begin boilerplate code '''
def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['DATABASE_URI'] = 'postgres://ooghcwqvooawaz:783d64f954ba54c0c7144c80e75ce659b5dd26c6435341702e1a466e202d3a68@ec2-54-173-77-184.compute-1.amazonaws.com:5432/dcpsit6sfoskj1'
  app.config['DBURI'] = 'postgres://ooghcwqvooawaz:783d64f954ba54c0c7144c80e75ce659b5dd26c6435341702e1a466e202d3a68@ec2-54-173-77-184.compute-1.amazonaws.com:5432/dcpsit6sfoskj1'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SQLITEDB'] = False
  app.config['SECRET_KEY'] = "SECRET"
  CORS(app)
  app.config['PREFERRED_URL_SCHEME'] = 'https'
  app.config['UPLOADED_PHOTOS_DEST'] = "uploads"
  app.config['UPLOAD_FOLDER'] = "uploads"
  photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
  login_manager.init_app(app) # uncomment if using flask login
  db.init_app(app)
  db.create_all(app=app)
  configure_uploads(app, photos)
  return app

app = create_app()

app.app_context().push()

''' End Boilerplate Code '''

@app.route('/', methods=['GET'])
def index():
  return render_template('login.html')

# SIGNUP FUNCTIONALITY
@app.route('/signup', methods=['GET'])
def signup():
  return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signupAction():
  data = request.form # get data from form submission
  newuser = User(username=data['username'], email=data['email']) # create user object
  newuser.set_password(data['password']) # set password
  try:
    db.session.add(newuser)
    db.session.commit() # save user
    login_user(newuser) # login the user
    flash('Account Created!')# send message
    return redirect(url_for('homepage'))# redirect to homepage
  except IntegrityError: # attempted to insert a duplicate user
    db.session.rollback()
    flash("Username or email already exists") # error message
  return redirect(url_for('signup'))


# LOGIN FUNCTIONALITY
@app.route('/login', methods=['GET'])
def login():
  return render_template('login.html')

@app.route('/login', methods=['POST'])
def loginAction():
  data = request.form
  user = User.query.filter_by(username = data['username']).first()
  if user and user.check_password(data['password']): # check credentials
    flash('Logged in.') # send message to next page
    login_user(user) # login the user
    return redirect(url_for('homepage')) # redirect to main page if login successful
  else:
    flash('Invalid username or password') # send message to next page
  return render_template('login.html')

#LOGOUT FUNCTIONALITY
@app.route('/logout', methods= ['GET'])
@login_required
def logout():
  logout_user()
  flash('Logged Out!')
  return redirect(url_for('login')) 

# HOMEPAGE
@app.route('/homepage', methods=['GET'])
def homepage():
  top_requests = Requests.query.limit(3).all()
  top_donations =  Donations.query.limit(3).all()
  return render_template('homepage.html', requests=top_requests,donations=top_donations)

# ALL REQUESTS FUNCTIONALITY
@app.route('/all_requests', methods=['GET'])
@login_required
def all_requests():
  requests = Requests.query.all()
  return render_template('all_requests.html', requests=requests) 

@app.route('/create_request', methods=['POST'])
@login_required
def create_request():
  data = request.form  #get form data 
  new_request = Requests(title=data['title'], body=data['body'], req_items=data['req_items'], userid=current_user.id)   #create request object
  db.session.add(new_request)
  db.session.commit() # save request
  flash('Request Created!')# send message

  #upload file functionality
  if 'file' not in request.files:
    flash('No file in request')
    return redirect(url_for('all_requests'))
  file = request.files['file']
  image = Request_Image(file, reqid=new_request.reqid)
  db.session.add(image)
  db.session.commit()

  return redirect(url_for('all_requests'))# redirect to homepage
  

  
# REQUEST PAGE
@app.route('/request_page/<int:id>', methods=['GET'])
@login_required
def request_page(id):
  request = Requests.query.filter_by(userid=current_user.id, reqid=id).first()    #find that request in  database
  if ',' in request.req_items:
    request.req_items = request.req_items.split(',')     #turn string into list of items
  return render_template('request_page.html', request=request)


# DONATE TO A REQUEST
@app.route('/donate/<int:id>', methods=['POST'])
@login_required
def donate(id):
  data = request.form  #get form data 
  req = Requests.query.filter_by(reqid=id).first()
  req.donated = True  #request has been donated to
  req.directions = data['directions']   #add input directions and note
  req.note =  data['note']
  req.donator_username = current_user.username  #get username and email of user who made donation
  req.donator_email = current_user.email
  db.session.add(req)
  db.session.commit()
  flash('Donation made.')
  return redirect(url_for('all_requests'))


# ALL DONATIONS FUNCTIONALITY
@app.route('/all_donations', methods=['GET'])
@login_required
def all_donations():
  donations = Donations.query.all()
  return render_template('all_donations.html', donations=donations) 

@app.route('/create_donation', methods=['POST'])
@login_required
def create_donation():
  data = request.form  #get form data 
  new_donation = Donations(title=data['title'], body=data['body'], don_items=data['don_items'], directions=data['directions'], note=data['note'], userid=current_user.id)   #create request object
  db.session.add(new_donation)
  db.session.commit() # save request
  flash('Donation Created!')# send message

  #upload file functionality
  if 'file' not in request.files:
    flash('No file in request')
    return redirect(url_for('all_donations'))
  file = request.files['file']
  image = Donation_Image(file, donid=new_donation.donid)
  db.session.add(image)
  db.session.commit()

  return redirect(url_for('all_donations'))# redirect to homepage


# DONATION PAGE
@app.route('/donation_page/<int:id>', methods=['GET'])
@login_required
def donation_page(id):
  donation = Donations.query.filter_by(userid=current_user.id, donid=id).first()    #find that donation in  database
  if ',' in donation.don_items:
    donation.don_items = donation.don_items.split(',')     #turn string into list of items
  return render_template('donation_page.html', donation=donation)

# REQUEST A DONATION
@app.route('/request/<int:id>', methods=['POST'])
@login_required
def make_request(id):
  data = request.form  #get form data 
  don = Donations.query.filter_by(donid=id).first()
  don.requested = True  #donation has been requested
  don.requestor_username = current_user.username  #get username and email of user who made donation
  don.requestor_email = current_user.email
  db.session.add(don)
  db.session.commit()
  flash('Donation requested.')
  return redirect(url_for('all_donations'))


# ABOUT US
@app.route('/about_us', methods=['GET'])
@login_required
def about_us():
  return render_template('about_us.html') 

# PROFILE 
@app.route('/profile', methods=['GET'])
@login_required
def profile():
  requests = Requests.query.filter_by(userid = current_user.id).all()
  donations = Donations.query.filter_by(userid = current_user.id).all()
  uploads = Upload.query.filter_by(userid=current_user.id).all()
  return render_template('profile.html', requests=requests, donations=donations, uploads=uploads)

@app.route('/upload', methods=['POST'])
def upload_action():
  if 'file' not in request.files:
    flash('No file in request')
    return redirect('/profile')
  file = request.files['file']
  newupload = Upload(file, userid=current_user.id)
  db.session.add(newupload)
  db.session.commit()
  flash('Document uploaded!')
  return redirect('/profile')

@app.route('/deleteUpload/<int:id>', methods=['GET'])
def delete_file(id):
  upload = Upload.query.get(id)
  if upload:
    upload.remove_file()
    db.session.delete(upload)
    db.session.commit()
    flash('Document deleted')
  return redirect('/profile')  

# CHANGE PROFILE INFO
@app.route('/change_profile/<int:id>', methods=['POST'])
@login_required
def change_profile(id):
  profile = User.query.filter_by(id=id).first()
  data = request.form
  if profile.check_password(data['old-password']):
    profile.set_password(data['new-password'])
  if data['username']:
    profile.username = data['username']
  db.session.add(profile)
  db.session.commit()
  flash('Change committed.')
  return redirect(url_for('profile'))





# ACCEPT/CANCEL DONATION
@app.route('/accept_cancel_donation/<int:id>', methods=['POST'])
@login_required
def accept_cancel_donation(id):
  req = Requests.query.filter_by(reqid=id).first()
  if request.form['button'] == 'Accept':     #if accepted, get request and delete it from db
    #send email if before cutoff date (After May 30th Gmail not allowing 3rd party signin)
    cutoff_date = datetime.datetime(2022, 5, 30)
    if datetime.datetime.now() < cutoff_date:
      # Create messages to send to requestor and donator
      requestor_message = '''Hello {},
      You have accepted a donation for your request entitled "{}".
      Requested items: {}
      Pickup Drections: {}
      Note: {}
      Donator Username: {}
      Donator Email: {}
      Be sure to stay safe when meeting to collect any items.
      Thank you for using GiveOne. 
      Best Wishes,
      The GiveOne Team'''.format(current_user.username, req.title, req.req_items, req.directions, req.note, req.donator_username, req.donator_email).encode("utf-8")
      donator_message = '''Hello {},
      Your donation to the request entitled "{}" has been accepted.
      Requested items: {}
      Pickup Drections: {}
      Note: {}
      Requestor Username: {}
      Requestor Email: {}
      Be sure to stay safe when meeting to donate any items.
      Thank you for using GiveOne. 
      Best Wishes,
      The GiveOne Team'''.format(req.donator_username, req.title, req.req_items, req.directions, req.note, current_user.username, current_user.email).encode("utf-8")
      # send messages via email
      server = smtplib.SMTP("smtp.gmail.com", 587)
      server.starttls()
      server.login("giveone1project@gmail.com", "GiveOne1!")
      server.sendmail("giveone1project@gmail.com", current_user.email, requestor_message) # send email to requestor
      server.sendmail("giveone1project@gmail.com", req.donator_email, donator_message)  # send email to donator
    db.session.delete(req)
    db.session.commit()
    flash('Donation accepted.')
  else:   # otherwise, remove donator info from request
    req.donated = False  
    req.directions = ""
    req.note =  ""
    req.donator_username = ""  
    req.donator_email = ""
    db.session.add(req)
    db.session.commit()
    flash('Donation canceled.')

  return redirect(url_for('profile'))

# ACCEPT/CANCEL REQUEST
@app.route('/accept_cancel_request/<int:id>', methods=['POST'])
@login_required
def accept_cancel_request(id):
  don = Donations.query.filter_by(donid=id).first()
  if request.form['button'] == 'Accept':     #if accepted, get request and delete it from db
    #send email if before cutoff date (After May 30th Gmail not allowing 3rd party signin)
    cutoff_date = datetime.datetime(2022, 5, 30)
    if datetime.datetime.now() < cutoff_date:
      # Create messages to send to requestor and donator
      donator_message = '''Hello {},
      You have accepted a request to your donation entitled "{}".
      Donated items: {}
      Pickup Drections: {}
      Note: {}
      Requestor Username: {}
      Requestor Email: {}
      Be sure to stay safe when meeting to donate any items.
      Thank you for using GiveOne. 
      Best Wishes,
      The GiveOne Team'''.format(current_user.username, don.title, don.don_items, don.directions, don.note, don.requestor_username, don.requestor_email)
      requestor_message = '''Hello {},
      Your request to the donation entitled "{}" has been accepted.
      Donated items: {}
      Pickup Drections: {}
      Note: {}
      Donator Username: {}
      Donator Email: {}
      Be sure to stay safe when meeting to collect any items.
      Thank you for using GiveOne. 
      Best Wishes,
      The GiveOne Team'''.format(don.requestor_username, don.title, don.don_items, don.directions, don.note, current_user.username, current_user.email)
      # send messages via email
      server = smtplib.SMTP("smtp.gmail.com", 587)
      server.starttls()
      server.login("giveone1project@gmail.com", "GiveOne1!")
      server.sendmail("giveone1project@gmail.com", current_user.email, donator_message) # send email to requestor
      server.sendmail("giveone1project@gmail.com", don.requestor_email, requestor_message)  # send email to donator
    db.session.delete(don)
    db.session.commit()
    flash('Request accepted.')
  else:   # otherwise, remove donator info from request
    don.requested = False  
    don.requestor_username = ""  
    don.requestor_email = ""
    db.session.add(don)
    db.session.commit()
    flash('Flash cancelled')

  return redirect(url_for('profile'))

# GET UPLOADED FILE FROM UPLOADS FOLDER
@app.route('/uploads/<path:name>', methods=["GET"])
def download_file(name):
  return send_from_directory('uploads', name)


#test
@app.route('/test', methods=["GET"])
def test():
  return render_template('test.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
