from zine_app.__init__ import app
from zine_app.models.user import User
from flask import render_template, request, flash, redirect, session, url_for
from zine_app.config.utils import UPLOAD_FOLDER,ALLOWED_EXTENSIONS


@app.route('/login_create')
def login_create():
    return(render_template('login_create.html'))


@app.route('/login', methods = ['POST'])
def login():
    data = request.form.to_dict()
    if User.validate_login(data):
        user = User.getUserByEmail(data['email'])
        session['id'] = user.id
        return(redirect(url_for('.user', profile_id = user.id)))
    else:
        print('failed to loginuser')
        return(redirect('/login_create'))
    
@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    session.clear();
    return(redirect('/login_create'))

    
@app.route('/viewprofile', methods =['post','get'])
def viewprofile():
    data = request.form.to_dict()
    id = data['id']
    return(redirect('/user/'+ f'{id}'))

@app.route('/register', methods = ['POST'])
def register():
    data = request.form.to_dict()
    if User.validate(data):
        user = User.insertUser(data)
        session['id'] = user
        return(redirect(url_for('.user', profile_id = user)))
    else:
        return(redirect('/login_create'))

@app.route('/user/<int:profile_id>')
def user(profile_id):
    if 'id' not in session:
        return(redirect(url_for('.login_create')))
    user = User.getUserById(profile_id)
    mainUser = User.getUserById(session['id'])
    
    return(render_template('user.html',profile_id = profile_id, user = user, mainUser=mainUser))


@app.route('/collect', methods = ['GET', 'POST'])
def collect():
    data = request.form.to_dict()
    print(data)
    if  not data['collection_id']:
        user = User.getUserById(session['id'])
        collection_name = 'user collection'
        result = user.createCollection(collection_name)
        print(result)
        collection_id = result
        user.collectZine(data['zine_id'],collection_id)
        return(redirect(url_for('.user', profile_id = user.id)))

        # make a generic collection called user collection.
    else:
        print('Collecting the zine')
        zine_id = data['zine_id']
        collection_id = data['collection_id']
        user = User.getUserById(session['id'])
        user.collectZine(zine_id,collection_id)
        return(redirect(url_for('.user', profile_id = user.id)))
    

@app.route('/request_friendship', methods = ['GET','POST'])
def request_friendship():
    data = request.form.to_dict()
    user_id = data['user_id']
    friend_id = data['friend_id']
    User.requestFriendship(user_id, friend_id)
    user = User.getUserById(session['id'])
    return(redirect(url_for('.user', profile_id = user.id)))


@app.route('/request_friendship/approve', methods = ['GET','POST'])
def request_friendship_approve():
    data = request.form.to_dict()
    friend_id = data['user_id']
    user_id = data['friend_id']
    User.requestFriendship(friend_id=friend_id, user_id=user_id)
    user = User.getUserById(session['id'])
    return(redirect(url_for('.user', profile_id = user.id)))
