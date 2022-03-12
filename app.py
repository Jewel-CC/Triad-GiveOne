import json
from flask import Flask,request,redirect,url_for,flash
from flask import render_template
from forms import SignUp,Login,newRequest,newDonation
from models import db,User,Giver,Getter,Request,Item
from flask_login import LoginManager, current_user, login_user,logout_user,login_required
from sqlalchemy.exc import IntegrityError


login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db.init_app(app)
login_manager.init_app(app)

app.app_context().push()
db.create_all(app=app)

#Login route, render login page
@app.route('/', methods=['GET'])
def index():
  form = LogIn()
  return render_template('login.html', form=form)

#user submits the login form
@app.route('/login', methods=['POST'])
def loginAction():
  form = LogIn()
  if form.validate_on_submit(): 
      data = request.form
      user = User.query.filter_by(username = data['username']).first()
      if user and user.check_password(data['password']): 
        flash('Logged in successfully.') 
        login_user(user) 
        return redirect(url_for('/')) #Edit to include redirect to main page
  flash('Invalid credentials')
  return redirect(url_for('index'))

#Signup route, render signup page
@app.route('/signup', methods=['GET'])
def signup():
  form = SignUp() 
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
    return redirect(url_for('index')) #Redirect to login page
  flash('Error invalid input!')
  return redirect(url_for('signup')) 

#Logout route
@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  flash('Logged Out!')
  return redirect(url_for('index')) 

@app.route("/test<name>", methods =['GET'])
def test(name):
	return render_template('test.html', name=name)


if __name__ == '__main__':
	app.run()

