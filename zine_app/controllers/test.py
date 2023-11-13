from zine_app.__init__ import app
from flask import render_template, request, flash, redirect, session, url_for
from zine_app.config.utils import UPLOAD_FOLDER,ALLOWED_EXTENSIONS




@app.route('/',methods = ['GET'])
def layout():
    print("rendering layout html")
    return(render_template('layout.html'))

# @app.route('/collect', methods = ['GET', 'POST'])
# def collect():
#     return(render_template('collect.html'))

# @app.route('/user_layout', methods=['GET'])
# def user_layout():
#     print("rendering the userlayout")
#     return(render_template('user_layout.html'))

# @app.route('/view_layout', methods = ['GET'])
# def view_layout():
#     return(render_template('view_layout.html'))

# @app.route('/login', methods = ['GET'])
# def login_create():
#     return(render_template('login_create.html'))

# @app.route('/user', methods=['GET'])
# def usert():
#     print("rendering the userlayout")
#     return(render_template('user.html'))