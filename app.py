import json
from flask import Flask,request,redirect,url_for,flash
from flask import render_template
from forms import SignUp,LogIn,newRequest,newDonation
from models import db,User, Item, Giver,Getter,Request
from flask_login import LoginManager, current_user, login_user,logout_user,login_required
from sqlalchemy.exc import IntegrityError



app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db.init_app(app)
# login_manager.init_app(app) 
app.app_context().push()
db.create_all(app=app)

@app.route('/', methods=['GET'])
def index():
  form = LogIn()
  return render_template('login.html', form=form)

@app.route('/login', methods=['POST'])
def loginAction():
  form = LogIn()
  if form.validate_on_submit(): # respond to form submission
      data = request.form
      user = User.query.filter_by(username = data['username']).first()
      if user and user.check_password(data['password']): # check credentials
        flash('Logged in successfully.') # send message to next page
        login_user(user) # login the user
        return redirect(url_for('all_requests')) # redirect to main page if login successful
  flash('Invalid credentials')
  return redirect(url_for('index'))


@app.route('/signup', methods=['GET'])
def signup():
  form = SignUp() # create form object
  return render_template('signup.html', form=form) # pass form object to template

@app.route('/signup', methods=['POST'])
def signupAction():
  form = SignUp() # create form object
  if form.validate_on_submit():
    data = request.form # get data from form submission
    newuser = User(username=data['username'], email=data['email']) # create user object
    newuser.set_password(data['password']) # set password
    db.session.add(newuser) # save new user
    db.session.commit()
    flash('Account Created!')# send message
    return redirect(url_for('index'))# redirect to login page
  flash('Error invalid input!')
  return redirect(url_for('signup'))  

@app.route('/all_requests', methods=['GET'])
def all_requests():
  return render_template('all_requests.html') 

@app.route('/donation_page', methods=['GET'])
def donation_page():
  return render_template('donation_page.html') 

@app.route('/request_page', methods=['GET'])
def request_page():
  return render_template('request_page.html') 

if __name__ == '__main__':
  app.debug = True
  app.run()
