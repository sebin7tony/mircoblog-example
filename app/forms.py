from flask.ext.wtf import Form
from wtforms import TextField,BooleanField,validators,DateField,IntegerField,TextAreaField
#from wtforms.validators import required

class LoginForm(Form):
	openid = TextField('openid', [validators.required()])
	remember_me = BooleanField('remember_me',default = False)

class SignUpForm(Form):
	username = TextField('Username',[validators.required()])
	email = TextField('email', [validators.Email(),validators.Length(min=6, max=120)])
	#email = TextField('Email', [validators.Length(min=6, max=120), validators.Email(),validators.Required])#error

class TaxForm(Form):
	startdate = DateField('startdate',[validators.required()])
	enddate  = DateField('enddate',[validators.required()])
	salary = IntegerField('salary',[validators.required()])

class EditForm(Form):
	nickname = TextField('nickname',[validators.required()] )
	about_me = TextAreaField('about_me',[validators.Length(min=0,max=120)])
