from app import app,lm,oid,db
from datetime import datetime
from flask import render_template,flash,redirect,url_for,request,session,g
from forms import LoginForm,SignUpForm,TaxForm,EditForm
from model import ROLE_USER,User
from flask.ext.login import login_required,login_user,current_user,logout_user

@app.route('/index', methods = ['GET','POST'])
@login_required
def index():
	user = g.user
	posts = [{'author' : {'name' : 'Savio'},'body' : 'this is a test'},
			{'author' : {'name' : 'Subin'},'body' : 'this is a test2'}]
	taxform = TaxForm()
	if taxform.validate_on_submit():
		startdate = taxform.startdate.data
		enddate = taxform.enddate.data
		salary = taxform.salary.data
		formdata = [startdate,enddate,salary]
		#formdata = "hello"
		flash("satrtdate :"+str(formdata[0])+" enddate : "+str(formdata[1]))
		#return redirect(url_for('.taxout', formdata = formdata))
	return render_template("index.html",form = taxform, user=user, posts=posts)


@app.route('/index/taxout', methods = ['GET','POST'])
def taxout():
	taxform = TaxForm()
	startdate = taxform.startdate.data
	enddate = taxform.enddate.data
	salary = taxform.salary.data
	formdata = [startdate,enddate,salary]
	#print formdata[1]
	return render_template("taxout.html",formdata = formdata)




@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))

	form = LoginForm()
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		return oid.try_login(form.openid.data,ask_for = ['nickname', 'email'])
	return render_template('login.html',form = form, providers = app.config['OPENID_PROVIDERS'])

@app.route('/edit', methods = ['GET','POST'])
@login_required
def edit():
	form = EditForm()
	if form.validate_on_submit():
		g.user.nickname = form.nickname.data
		g.user.about_me = form.about_me.data
		db.session.add(g.user)
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('user',nickname = g.user.nickname))
	else:
		form.nickname.data = g.user.nickname
		form.about_me.data = g.user.about_me
	return render_template('edit.html',
        form = form)
    

@oid.after_login
def after_login(resp):
	if resp.email is None or resp.email=="":
		flash("Invalid login !!")
		return redirect(url_for('/login'))
	user = User.query.filter_by(email = resp.email).first()
	if user is None:
		nickname = resp.nickname
		if nickname is None or nickname == "":
			nickname = resp.email.split('@')[0]
		user = User(nickname = nickname,email = resp.email,role = ROLE_USER)
		db.session.add(user)
		db.session.commit()
	remember_me = False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me',None)
	login_user(user,remember = remember_me)
	return redirect(request.args.get('next') or url_for('index'))


@app.before_request	
def before_request():
	g.user = current_user
	if g.user.is_authenticated:
		g.user.last_seen = datetime.utcnow()
		#db.session.add(g.user)
		#db.session.commit()

@app.route('/logout')
def logout():
	logout_user()
	g.user = None
	return redirect(url_for('login'))


@app.route('/signup' , methods = ['GET','POST'])
def signUp():
	form = SignUpForm()
	if form.validate_on_submit():
		print "test string"
		flash('signup done with '+form.email.data)
		return redirect(url_for('index'))
	return render_template('signup.html',form = form )



@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
	user = User.query.filter_by(nickname = nickname).first()
	if user == None:
		flash('User' + nickname + 'is not found')
		redirect(url_for('index'))
	posts = [{'author': user,'body' : 'this is post 1'},
			 {'author': user,'body' : 'this is post 2'}]
	return render_template('user.html',user = user, post = posts)
	



