from flask import render_template, redirect, url_for, request, current_app,session
from flask.ext.login import login_user, logout_user, login_required
from .. import db 
from ..models import Todo, Category 
from . import todo

# view functions 
@todo.route('/')
@todo.route('/todo/')
@todo.route('/index/')
def index():
    todos = Todo.query.filter(Todo.status == False).all()
    dones = Todo.query.filter(Todo.status == True).all()
    categories = Category.query.all()
    return render_template('index.html',todos = todos, dones = dones, categories=categories )

@todo.route('/todo/new', methods=['POST'])
@login_required
def new():
    title = request.form['title']
    category = request.form['category']
    c = Category.query.filter(Category.name == category).first()
    
    todo = Todo(title, c)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('todo.index'))

@todo.route('/todo/category/new', methods=['POST'])
@login_required
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
        
    return redirect(url_for('todo.index'))
    
@todo.route('/todo/del/<int:id>')
@login_required
def delete(id):
    todo = Todo.query.get(id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('todo.index'))
    
@todo.route('/todo/done/<int:id>')
@login_required
def done(id):
    todo = Todo.query.get(id)
    if todo:
        todo.status = True
        db.session.commit()
    return redirect(url_for('todo.index'))
    
@todo.route('/todo/retrieve/<int:id>')
@login_required
def retrive(id):
    todo = Todo.query.get(id)
    if todo:
        todo.status = False
        db.session.commit()
    return redirect(url_for('todo.index'))

@todo.route('/todo/category/<name>')
def category(name):

    categories = Category.query.all()
    category = Category.query.filter(Category.name == name).first()
    
    todos = category.todos.filter(Todo.status == False).all()  # This is controlled by backref 
    dones = category.todos.filter(Todo.status == True).all()
    
    return render_template('index.html',todos = todos, dones = dones, categories = categories )


