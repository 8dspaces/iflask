from . import db 
from datetime import datetime

# used by auth
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import login_manager

class Todo(db.Model):
    
    __tablename__ = 'todo'
    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80), nullable = False) 
    post_date = db.Column(db.DateTime)
    status = db.Column(db.Boolean(), default = False)
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref = db.backref('todos',lazy='dynamic'))
    
    def __init__(self, title, category = None, post_date = None, status = False):
        self.title = title 
        self.category = category 
        if post_date is None:
            post_date = datetime.utcnow()
        self.post_date = post_date 
        self.status = status
    
    def __repr__(self):
        
        return '<Todo %r>' % self.title 
        
    
    
class Category(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False) 
    
    def __init__(self, name ):
        self.name = name
    
    def __repr__(self):
        return '<Category %r>' % self.name
        
        
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))