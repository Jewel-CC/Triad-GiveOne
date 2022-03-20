import json
from flask import Flask,request,redirect,url_for,flash
from flask import render_template
from forms import SignUp,Login,newRequest,newDonation
from models import db,User, Item, Giver,Getter,Request
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

@app.route("/")
@login_required
def home():
	return render_template('index.html')

if __name__ == '__main__':
  app.debug = True
  app.run()
