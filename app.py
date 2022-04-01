from flask import Flask, request, jsonify, render_template, redirect, flash, url_for, jsonify, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from datetime import timedelta
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
import os

from models import db, User, Requests, Donations, Upload

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


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<path:name>', methods=["GET"])
def download_file(name):
  return send_from_directory('uploads', name)

@app.route('/profile', methods=['GET'])
def uploader():
  uploads = Upload.query.all()
  return render_template('profile.html', uploads=uploads)

@app.route('/upload', methods=['POST'])
def upload_action():
  if 'file' not in request.files:
    flash('No file in request')
    return redirect('/uploader')
  file = request.files['file']
  newupload = Upload(file)
  db.session.add(newupload)
  db.session.commit()
  flash('file uploaded!')
  return redirect('/profile')

@app.route('/deleteUpload/<int:id>', methods=['GET'])
def delete_file(id):
  upload = Upload.query.get(id)
  if upload:
    upload.remove_file()
    db.session.delete(upload)
    db.session.commit()
    flash('Upload Deleted')
  return redirect('/profile')  



@app.route('/home', methods=['GET'])
def home():
  return render_template('homepage.html')

@app.route('/about', methods=['GET'])
def about_us():
  return render_template('about_us.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
