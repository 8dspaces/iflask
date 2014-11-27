from flask import Flask, render_template, session, redirect, url_for, flash,request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from datetime import datetime
from werkzeug import secure_filename
import os 

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'test.db')
SECRET_KEY = '\xf0\xe4},\x8f\x10\xe3.\x13?\x9eP\xcd!\xb1\x17\xa2%\xbbU'

app = Flask(__name__)
app.config.from_object(__name__) 
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

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

# view functions 
@app.route('/')
@app.route('/todo/')
@app.route('/index/')
def index():
    todos = Todo.query.filter(Todo.status == False).all()
    dones = Todo.query.filter(Todo.status == True).all()
    categories = Category.query.all()
    return render_template('index.html',todos = todos, dones = dones, categories=categories )

@app.route('/todo/new', methods=['POST'])
def new():
    title = request.form['title']
    category = request.form['category']
    c = Category.query.filter(Category.name == category).first()
    
    todo = Todo(title, c)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/todo/category/new', methods=['POST'])
def category_new():
    name = request.form['name']
    c = Category.query.filter(Category.name == name).first()
    
    if c:
        flash("Category already exist!")
    else:
        category = Category(name)
        db.session.add(category)
        db.session.commit()
        flash("Category be created successfully!")
        
    return redirect(url_for('index'))
    
@app.route('/todo/del/<int:id>')
def delete(id):
    todo = Todo.query.get(id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('index'))
    
@app.route('/todo/done/<int:id>')
def done(id):
    todo = Todo.query.get(id)
    if todo:
        todo.status = True
        db.session.commit()
    return redirect(url_for('index'))
    
@app.route('/todo/retrieve/<int:id>')
def retrive(id):
    todo = Todo.query.get(id)
    if todo:
        todo.status = False
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/todo/category/<name>')
def category(name):

    categories = Category.query.all()
    category = Category.query.filter(Category.name == name).first()
    
    todos = category.todos.filter(Todo.status == False).all()  # This is controlled by backref 
    dones = category.todos.filter(Todo.status == True).all()
    
    return render_template('index.html',todos = todos, dones = dones, categories = categories )

# handle picture related view functions 



@app.route('/view/pics/<filename>')
def view_pic(filename):
    return render_template('view_pic.html', filename = filename)
    
#@app.route('/pic/upload', methods = ['POST'])
@app.route('/pic/',methods = ['POST', 'GET'])
@app.route('/pic/<int:page>',methods = ['POST', 'GET'])
def pictures( page= 0):
    if request.method == 'POST':
        f = request.files['pic']
        f.save(os.path.join(basedir, 'static/pics/'+secure_filename(f.filename)))
        return redirect(url_for('pictures'))
    else:
        pics = os.listdir(basedir + '/static/pics')
        pics = [i for i in pics if i[-4:] in ['.png','.jpg','.bmp']]
        pages = (len(pics)+13)/12
        pics = pics[page*12:page*12+12]
        return render_template('pictures.html', pics = pics, page =page, pages=pages)

#@app.route('/pic')
#def pictures():
#    pics = os.listdir(basedir + '/static/pics')
#    pics = [i for i in pics if i[-4:] in ['.png','.jpg','.bmp']]
#    return render_template('pictures.html', pics = pics)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

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
    #db.create_all()
    #create_database()
    app.run(debug = True)
