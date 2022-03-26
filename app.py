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
  return render_template('signup.html')

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

#LOGOUT FUNCTIONALITY
@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  flash('Logged Out!')
  return redirect(url_for('login')) 

# REQUESTS FUNCTIONALITY
@app.route('/all_requests', methods=['GET'])
@login_required
def all_requests():
  return render_template('all_requests.html') 


# DONATIONS FUNCTIONALITY
@app.route('/all_donations', methods=['GET'])
@login_required
def all_donations():
  return render_template('all_donations.html') 

@app.route('/about_us', methods=['GET'])
@login_required
def about_us():
  return render_template('about_us.html') 


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)