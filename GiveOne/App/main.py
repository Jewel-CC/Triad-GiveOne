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

#------Login--------------------------	----------------------#
#login
@app.route('/', methods=['GET'])
def index():
    form = Login()
    return render_template('login.html', form=form)

#Link login form to login action
@app.route('/login', methods=['POST'])
def loginAction():
    form = Login()
    if form.validate_on_submit(): 
        data = request.form
        user = User.query.filter_by(username = data['username']).first()
        if user and user.check_password(data['password']): 
          flash('Successfully logged in!') 
          login_user(user) 
          return redirect(url_for('index')) 
    flash('Wrong email/password!')
    return redirect(url_for('index'))


@app.route("/home")
@login_required
def home():
	  return render_template('index.html')