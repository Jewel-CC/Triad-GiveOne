from flask import Flask, request, jsonify, render_template, redirect, flash, url_for, jsonify
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from sqlalchemy.exc import IntegrityError

from models import db, User, Requests, Donations

''' Begin Flask Login Functions '''
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

''' End Flask Login Functions '''

''' Begin boilerplate code '''
def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = "MYSECRET"
  CORS(app)
  login_manager.init_app(app) # uncomment if using flask login
  db.init_app(app)
  db.create_all(app=app)
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
    return redirect(url_for('all_requests'))# redirect to homepage
  except IntegrityError: # attempted to insert a duplicate user
    db.session.rollback()
    flash("username or email already exists") # error message
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
    flash('Logged in successfully.') # send message to next page
    login_user(user) # login the user
    return redirect(url_for('all_requests')) # redirect to main page if login successful
  else:
    flash('Invalid username or password') # send message to next page
  return render_template('login.html')


# ALL REQUESTS FUNCTIONALITY
@app.route('/all_requests', methods=['GET'])
@login_required
def all_requests():
  requests = Requests.query.all()
  for request in requests:
    request.body = request.body[0:50]
  return render_template('all_requests.html', requests=requests) 

@app.route('/create_request', methods=['POST'])
@login_required
def create_request():
  data = request.form  #get form data 
  new_request = Requests(title=data['title'], body=data['body'], req_items=data['req_items'], userid=current_user.id)   #create request object
  db.session.add(new_request)
  db.session.commit() # save request
  flash('Request Created!')# send message
  return redirect(url_for('all_requests'))# redirect to homepage
  


# REQUEST PAGE
@app.route('/request_page/<int:id>', methods=['GET'])
@login_required
def request_page(id):
  request = Requests.query.filter_by(userid=current_user.id, reqid=id).first()    #find that request in  database
  if ',' in request.req_items:
    request.req_items = request.req_items.split(',')     #turn string into list of items
  return render_template('request_page.html', request=request)


# ALL DONATIONS FUNCTIONALITY
@app.route('/all_donations', methods=['GET'])
@login_required
def all_donations():
  donations = Donations.query.all()
  for donation in donations:
    donation.body = donation.body[0:50]
  return render_template('all_donations.html', donations=donations) 

@app.route('/create_donation', methods=['POST'])
@login_required
def create_donation():
  data = request.form  #get form data 
  new_donation = Donations(title=data['title'], body=data['body'], don_items=data['don_items'], directions=data['directions'], note=data['note'], userid=current_user.id)   #create request object
  db.session.add(new_donation)
  db.session.commit() # save request
  flash('Donation Created!')# send message
  return redirect(url_for('all_donations'))# redirect to homepage


# DONATION PAGE
@app.route('/donation_page/<int:id>', methods=['GET'])
@login_required
def donation_page(id):
  donation = Donations.query.filter_by(userid=current_user.id, donid=id).first()    #find that donation in  database
  if ',' in donation.don_items:
    donation.don_items = donation.don_items.split(',')     #turn string into list of items
  return render_template('donation_page.html', donation=donation)

@app.route('/about_us', methods=['GET'])
@login_required
def about_us():
  return render_template('about_us.html') 

@app.route('/profile', methods=['GET'])
@login_required
def profile():
  return render_template('profile.html')

# LOGOUT USER
@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  flash('Logged Out!')
  return redirect(url_for('login')) 

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)