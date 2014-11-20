from flask import Flask 
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import os 

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'test.db')

app = Flask(__name__)
app.config.from_object(__name__) 
db = SQLAlchemy(app)


class Todo(db.Model):
    
    __tablename__ = 'todo'
    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80), nullable = False) 
    post_date = db.Column(db.DateTime)
    status = db.Column(db.Boolean(), default = False)
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref = db.backref('todos',lazy='dynamic'))
    
    def __init__(self, title, category, post_date = None, status = False):
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
        return 

# view functions 
@app.route('/')
@app.route('/index/')
def index():

    return ''.join('+++'.join([x.title for x in Todo.query.all()]))
        

def create_database():
    c = Category('python')
    c1 = Category('flask')
    t1 = Todo('I love Python', c)
    t2 = Todo('I love Flask', c1)
    t3 = Todo('I love Flask very much', c)

    db.session.add(c)
    db.session.add(c1)
    db.session.commit()

    db.session.add(t1)
    db.session.add(t2)
    db.session.add(t3)
    db.session.commit()

if __name__ == '__main__':
    #create_database()
    app.run(debug = True)
