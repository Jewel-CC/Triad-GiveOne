import os
from flask import Flask, render_template, redirect, flash, url_for
#from flask_jwt import JWT
from datetime import timedelta 
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, login_required
from sqlalchemy.exc import IntegrityError

from App.models import db, User

from flask_uploads import (
    UploadSet, 
    configure_uploads, 
    IMAGES, 
    TEXT, 
    DOCUMENTS
)

from App.views import (
    api_views,
    user_views
)

#place all views here
views = [api_views, user_views]

def add_views(app, views):
    for view in views:
        app.register_blueprint(view)


def loadConfig(app, config):
    app.config['ENV'] = os.environ.get('ENV', 'development')
    if app.config['ENV'] == "development":
        app.config.from_object('App.config')
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        app.config['JWT_EXPIRATION_DELTA'] = os.environ.get('JWT_EXPIRATION_DELTA')
        app.config['DEBUG'] = os.environ.get('DEBUG')
        app.config['ENV'] = os.environ.get('ENV')

    for key,value in config.items():
        app.config[key] = config[key]
        
        
###
#''' Set up JWT here (if using flask JWT)'''
#def authenticate(email, password):
  #user = User.query.filter_by(email=email).first()
  #if user and user.check_password(password):
    #return user

#Payload is a dictionary which is passed to the function by Flask JWT
#def identity(payload):
  #return User.query.get(payload['identity'])


#''' End JWT Setup '''
###

###Implementing Flask-login###
#Start
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
###End##

def init_db(app):
    db.init_app(app)
    db.create_all(app=app)

def create_app(config={}):
    app = Flask(__name__, static_url_path='/static')
    loadConfig(app, config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "SECRET"
    CORS(app)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app, views)  
    login_manager.init_app(app)    
    app.app_context().push()
    return app

if __name__ == "__main__":
    app = create_app()
    init_db(app)
    
    
###Start All account related routes:###

#login
@app.route('/login', methods=['GET'])
def index():
  form = LogIn()
  return render_template('login.html', form=form)

#Link login form to login action
@app.route('/login', methods=['POST'])
def loginAction():
  form = LogIn()
  if form.validate_on_submit(): 
      data = request.form
      user = User.query.filter_by(username = data['username']).first()
      if user and user.check_password(data['password']): 
        flash('Logged in successfully.') 
        login_user(user) 
        return redirect(url_for('todos')) 
  flash('Invalid credentials')
  return redirect(url_for('index'))

#logout
@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  flash('Logged Out!')
  return redirect(url_for('index')) 

#signup
@app.route('/signup', methods=['GET'])
def signup():
  form = SignUp() # create form object
  return render_template('signup.html', form=form) 

@app.route('/signup', methods=['POST'])
def signupAction():
  form = SignUp() 
  if form.validate_on_submit():
    data = request.form 
    newuser = User(username=data['username'], email=data['email']) 
    newuser.set_password(data['password']) 
    db.session.add(newuser) 
    db.session.commit()
    flash('Account Created!')
    return redirect(url_for('index'))
  flash('Error invalid input!')
  return redirect(url_for('signup')) 


#homepage
@app.route('/', methods=['GET'])
def index():

  return render_template('index.html')

###End###
