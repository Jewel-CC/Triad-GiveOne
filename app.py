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


@app.route("/home")
@login_required
def home():
	acts = Activity.query.all()
	return render_template('HomePage.html',acts = acts)

#@app.route("/forum", methods=['GET'])
#@login_required
#def forum():
#	form = NewPost()
#	Posts = Post.query.all()
#	return render_template('Forum.html',form = form, posts = Posts)

#-------Forum----------------------------------------------------------------#

@app.route("/forum", methods=['GET'])
@login_required
def allTopics():
	form = NewTopic()
	form1 = NewPost()
	topic = request.args.get('topic')
	if topic:
		post = Post.query.filter_by(topic = topic)
		return render_template('Forum.html',form=form1,posts = post,topic = topic)
	Topics = Topic.query.all()
	return render_template('All Topics.html',form = form, Topics = Topics)

@app.route("/forum", methods=['POST'])
@login_required
def newPost():
	form = NewPost()
	topic = request.args.get('topic')
	if form:
		data = request.form
		newPost = Post(content = data['content'], topic = topic, author = current_user.username)
		activity = Activity(name = current_user.username, type = 'p', topic = newPost.topic)
		db.session.add(newPost)
		db.session.add(activity)
		db.session.commit()
		return redirect(request.referrer)
	return redirect(request.referrer)

#------Start a new Topic----------------------------------------------------#
@app.route("/addTopic", methods=['GET'])
@login_required
def newTopic():
	form = NewTopic()
	return render_template('newTopic.html',form = form)

@app.route("/addTopic", methods=['POST'])
@login_required
def addTopic():
	form = NewTopic()
	if form:
		data = request.form
		newTopic = Topic(Title = data['title'],content = data['content'])
		newPost = Post(content = data['content'],topic = data['title'],author = current_user.username)
		activity = Activity(name = current_user.username, type = 't', topic = newPost.topic)
		db.session.add(newTopic)
		db.session.add(newPost)
		db.session.add(activity)
		db.session.commit()
		return redirect(url_for('allTopics'))
	return redirect(url_for('allTopics'))
	
#---------------------------------------------------------------------------------------#

#---------Delete------------------------------------------------------------------------#
@app.route("/deletep")
@login_required
def delete():
	delete = request.args.get('del')
	if delete:
		post= Post.query.filter_by(id = delete ).first()
		db.session.delete(post)
		db.session.commit()
		return redirect(request.referrer)

#-------Update-------------------------------------------------------------------------#
@app.route("/updatep")
@login_required
def update():
	update = request.args.get('update')
	form = NewPost()
	if update :
		up = Post.query.filter_by(id = update).first()
		return render_template('update.html',update = up,form = form)

@app.route("/updatep", methods=['POST'])
@login_required
def updateP():
	form = NewPost()
	id = request.args.get('id')
	if id:
		data = request.form
		post = Post.query.filter_by(id = id).first()
		post.content = data['content']	
		topic = post.topic
		db.session.add(post)
		db.session.commit()
		return redirect("/forum?topic=%s" %topic)
	return redirect("/forum")
#--------------------------------------------------------------------------------------#




#------Workouts------------------------------------------------------------------------#


@app.route("/workouts",methods=['GET'])
@login_required
def workouts():
	workouts = Workout.query.filter_by()
	return render_template('Workout.html', workouts = workouts)

@app.route("/newworkout",methods=['GET'])
@login_required
def create_Workout():
	form = NewWorkout()
	return render_template('NewWorkout.html', form = form)

@app.route("/newworkout",methods=['POST'])
@login_required
def post_Workout():
	form = NewWorkout()
	data = request.form
	workout = Workout( author = current_user.username, name = data["Title"],E1 =data["Excercise1"],E2 =data["Excercise2"],E3 =data["Excercise3"],E4 = data["Excercise5"],E5 =data["Excercise5"],S1 = data["Sets1"],S2 = data["Sets2"],S3 = data["Sets3"],S4 = data["Sets4"],S5 = data["Sets5"],R1 = data["Reps1"],R2 = data["Reps2"],R3 = data["Reps3"],R4 = data["Reps4"],R5 = data["Reps5"])
	activity = Activity(name = current_user.username, type = 'w',topic = data["Title"])
	db.session.add(workout)
	db.session.add(activity)
	db.session.commit()
	
	return redirect(url_for("workouts"))

@app.route("/workoutDetails",methods=['GET'])
@login_required
def workoutDetails():
	wrk = request.args.get('wrk')
	workout = Workout.query.filter_by(id=wrk).first()

	return render_template('workoutDetails.html',wrk = workout)

#---------------------------------------------------------------------------------------#


if __name__ == '__main__':
	app.run()

