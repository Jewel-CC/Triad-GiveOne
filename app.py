import json
from flask import Flask,request,redirect,url_for
from flask import render_template
from forms import SignUp,Login,NewPost,NewTopic,NewWorkout
from models import db,User,Post,Topic,Workout,Activity
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

@app.route("/", methods =['GET'])
def login():
	form = Login()
	return render_template('index.html', form = form)

@app.route("/login", methods =['POST'])
def loginUser():
	form = Login()
	data = request.form
	user = User.query.filter_by(username = data['username']).first()
	if user and user.check_password(data['password']):
		login_user(user)
		return redirect(url_for('home'))
	return render_template('index.html', form = form)

#------------------------------------------------------------

#--------SIGN UP--------------------------------------------#

@app.route("/signup", methods=['GET'])
def signup():
	form = SignUp()
	return render_template('SignUp.html', form = form)

@app.route("/signup", methods=['POST'])
def newUser():
	form = SignUp()
	if form:
		data = request.form
		newUser = User(username = data['username'], email = data['email'])
		newUser.set_password(data['password'])
		db.session.add(newUser)
		db.session.commit()
		return redirect(url_for('login'))
	return redirect(url_for('signup'))

#-----------------------------------------------------------#

#--------LogOut---------------------------------------------#

@app.route("/logout", methods =['GET'])
@login_required
def LogOut():
	logout_user()
	return redirect(url_for('login'))
#----------------------------------------------------------#


@app.route("/test<name>", methods =['GET'])
def test(name):
	return render_template('test.html', name=name)


if __name__ == '__main__':
	app.run()

