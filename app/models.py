from . import db 
from datetime import datetime

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