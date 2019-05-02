from time import time
import jwt
from datetime import datetime 
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from app import db , login, app


@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))

	posts = db.relationship('Post', backref='post', lazy='dynamic')

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode(
			{'reset_password': self.id, 'exp': time() + expires_in}, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
		except:
			return
		return User.query.get(id)

	def __repr__(self):
		return '<User {}>'.format(self.username)


tags = db.Table('tags',
	db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
	db.Column('page_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
	)

class Post(db.Model):
	"""	tag = relationship("Tag", back_populates="Post")"""
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(140))
	body = db.Column(db.String(140))
	like = db.Column(db.Integer, default=0)
	dislike = db.Column(db.Integer, default=0)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	image_path = db.Column(db.String(250))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User')
	tags = db.relationship('Tag', secondary=tags, lazy='subquery',
			backref=db.backref('posts', lazy=True))

	def __repr__(self):
		return '<Post {} - {}>'.format(self.title, self.tags)



class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

	def __repr__(self):
		return self.body

class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(145))

	def __repr__(self):
		return '{} - {}'.format(self.id, self.body)

