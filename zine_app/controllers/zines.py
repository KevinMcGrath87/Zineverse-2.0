from zine_app.models.zine import Zine
from zine_app.__init__ import app
from flask import render_template, redirect, session, flash, request,url_for
import os
from werkzeug.utils import secure_filename


@app.route('/create_zine', methods = ['POST'])
def create_zine():
    data = request.form.to_dict()
    data['author_id']=session['id']
    # data['author'] = User.getUserById(session['id']).username
    Zine.createZine(data, session['id'])
    return(redirect(url_for('.user', profile_id= session['id'])))


@app.route('/upload', methods = ['POST', 'UPDATE'])
def upload():
    print("upload route")
    zine_id = request.form['zine']
    user_id = session['id']
    if 'file' not in request.files:
        flash('no file')
        return(redirect(url_for('user',profile_id = user_id)))
    file = request.files['file']
    if not Zine.upload(file, zine_id):
        flash('issue with upload of file')
    else:
        return(redirect(url_for('user',profile_id = user_id)))

@app.route('/view', methods = ['GET','POST'])
def view():
    data = request.form.to_dict()
    zine_id = data['zine_id']
    page = 0
    return(redirect(url_for('viewpage',zine_id = zine_id, page = page)))

@app.route('/viewpage/<int:zine_id>/<int:page>')
def viewpage(zine_id, page):
    zine = Zine.getZine(zine_id)
    path = zine.path
    pages = os.listdir(path)
    filename = path.rsplit("zinelib\\",1)[1]
    if pages:
        return(render_template("view.html", pages = pages, filename= filename, page = page,zine_id = zine_id))
    else:
        return(redirect(url_for('user',profile_id = session['id'])))
    

@app.route('/page_turn/<int:page>/<int:length>/<int:zine_id>', methods = ['POST'])
def page_turn(page, length, zine_id):
    data = request.form.to_dict()
    if data['click'] == 'left'and page > 0:
        page -= 1
    if data['click'] == 'right' and page < length - 1:
        page += 1
    return redirect(url_for('.viewpage',zine_id = zine_id, page = page))



