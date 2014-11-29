from flask import render_template, redirect, url_for, request, current_app,session
from . import pic
import os 
from werkzeug import secure_filename

# handle picture related view functions 

@pic.route('/pic/',methods = ['POST', 'GET'])
@pic.route('/pic/<int:page>',methods = ['POST', 'GET'])
def pictures( page= 0):
    if request.method == 'POST':
        f = request.files['pic']
        f.save('./app/static/pics/'+secure_filename(f.filename))
        return redirect(url_for('pic.pictures'))
    else:
        pics = os.listdir('./app/static/pics/')
        pics = [i for i in pics if i[-4:] in ['.png','.jpg','.bmp']]
        pages = (len(pics)+13)/12
        pics = pics[page*12:page*12+12]
        return render_template('pictures.html', pics = pics, page =page, pages=pages)

@pic.route('/view/pics/<filename>')
def view_pic(filename):
    return render_template('view_pic.html', filename = filename)
