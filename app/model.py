from app import db

ROLE_ADMIN = 1
ROLE_USER = 2

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	nickname = db.Column(db.String(64))
	email = db.Column(db.String(60),index = True, unique = True)
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	posts = db.relationship('Post',backref = 'auther', lazy = 'dynamic')
	about_me = db.Column(db.String(120))
	last_seen = db.Column(db.DateTime)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' % (self.nickname)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey(User.id))

	def __repr__(self):
		return '<Post %r>' %(self.body)