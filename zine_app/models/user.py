from flask import flash
from zine_app.__init__ import app
from zine_app.models.collection import Collection
from zine_app.config.mysqlconnection import connectToMySQL
from zine_app.config.utils import DATABASE
import re
REGEX_EMAIL = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
REGEX_PW_FORM = re.compile(r'\S\w+\d+[!@#$/*]+')
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

db = DATABASE


class User:
    def __init__(self, data):
        self.id = data['id']
        self.dob = data['dob']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.update_at = data['updated_at']
        self.zines = []
        self.friends = []
    
    def intersection(self, list1,list2):
        list3 = []
        for each in list1:
            if each not in list2:
                list3.append(each)
        for each in list2:
            if each not in list1:
                list3.append(each)
        return(list3)
    

    def getZines(self):
        query = 'SELECT * from zines WHERE zines.author_id = %(id)s'
        data={'id':self.id}
        result = connectToMySQL(db).query_db(query,data)
        return(result)
    
    def createCollection(self,collection_name):
        return( Collection.createNew(self.id, collection_name))

    
    def getFriends(self):
        query = 'SELECT * FROM users as usersfriends INNER JOIN friendships ON usersfriends.id = friendships.user_id1 INNER JOIN users ON users.id = friendships.user_id2 WHERE users.id = %(id)s'
        data = {'id':self.id}
        result = connectToMySQL(db).query_db(query, data)
        leftsided = []
        if result:
            for each in result:
                leftId = each['id']
                leftsided.append(leftId)
        query = 'SELECT * FROM users as usersfriends INNER JOIN friendships on friendships.user_id2 = usersfriends.id INNER JOIN users on users.id = friendships.user_id1 WHERE users.id = %(id)s'
        result = connectToMySQL(db).query_db(query, data)
        rightsided = []
        if result:
            for each in result:
                rightId = each['id']
                rightsided.append(rightId)
        friends = []
        for each in leftsided:
            if (each in rightsided):
                friends.append(User.getUserById(each))
        return(friends)

    def requestsPendingUserApproval(self):
        query = 'SELECT * FROM users as usersfriends INNER JOIN friendships ON usersfriends.id = friendships.user_id1 INNER JOIN users ON users.id = friendships.user_id2 WHERE users.id = %(id)s'
        data = {'id':self.id}
        result = connectToMySQL(db).query_db(query, data)
        friends = self.getFriends()
        friend_ids=[]
        for friend in friends:
            friend_ids.append(friend.id)
        left_ids = []    
        if result:
            for each in result:
                each = each['id']
                left_ids.append(each)
        leftsided = []
        intersection = self.intersection(left_ids,friend_ids)
        for each in intersection:
            leftsided.append(User.getUserById(each))
        print("requests pending",leftsided)
        return(leftsided)

    def pendingRequestsByUser(self):
        friends = self.getFriends()
        friend_ids=[]
        for friend in friends:
            friend_ids.append(friend.id)
        data = {'id':self.id}
        query = 'SELECT * FROM users as usersfriends INNER JOIN friendships on usersfriends.id = friendships.user_id2   INNER JOIN users on users.id = friendships.user_id1 WHERE users.id = %(id)s'
        result = connectToMySQL(db).query_db(query, data)
        right_ids =[]
        if result:
            for each in result:
                each = each['id']
                right_ids.append(each) 
        print('pending ids',right_ids)
        print('friend ids', friend_ids)
        intersection = self.intersection(friend_ids, right_ids)
        rightsided = []
        for each in intersection:
            rightsided.append(User.getUserById(each))
        return(rightsided)




        # onesided = []
        # onesideRequested = []
        #     else: 
        #         onesided.append(User.getUserById(each))
        # for each in rightsided:
        #     if not (each in leftsided):
        #         onesideRequested.append(User.getUserById(each))

        # return([currentUser.friends,onesided,onesideRequested])
    
    def getCollections(self):
        query= 'SELECT * from collections WHERE collections.user_id = %(id)s'
        data = {'id':self.id}
        result = connectToMySQL(db).query_db(query,data)
        collections = []
        for dict in result:
            collections.append(Collection(dict))
        return(collections)
    
    def collectZine(self, zine_id, collection_id):
        data = {}
        data['zine_id']=zine_id
        data['user_id']=self.id
        # query = "INSERT INTO collections(user_id,zine_id) VALUES (%(user_id)s,%(zine_id)s)WHERE collection.id= %(collection_id)s"
        # result = connectToMySQL(db).query_db(query,data)
        data['collection_id']=collection_id
        query = "INSERT INTO collected(zine_id, collection_id) VALUES (%(zine_id)s, %(collection_id)s)"
        result = connectToMySQL(db).query_db(query,data)
        return(result)
    
    @classmethod
    def requestFriendship(cls,user_id, friend_id):
        query = 'INSERT into friendships (user_id1,user_id2) VALUES(%(user_id1)s, %(user_id2)s)'
        data={'user_id1':user_id, 'user_id2':friend_id}
        result = connectToMySQL(db).query_db(query,data)
        return(result)


    @classmethod
    def approveRequest(cls, id):
        pass


    @classmethod
    def getUserById(cls,id):
        query = 'SELECT * FROM users WHERE users.id = %(id)s'
        data = {'id': id}
        result = connectToMySQL(db).query_db(query, data)
        return(cls(result[0]))
    
    @classmethod
    def getUserByEmail(cls,email):
        query = 'SELECT * FROM users WHERE users.email = %(email)s'
        data = {'email': email}
        result = connectToMySQL(db).query_db(query, data)
        if result:
            return(cls(result[0]))
        else:
            return None
    
    @classmethod
    def insertUser(cls, data):
        query = 'INSERT INTO users (username, email, password, dob) VALUES(%(username)s,%(email)s, %(password)s, %(dob)s)'
        data['password']= bcrypt.generate_password_hash(data['password'])
        user = connectToMySQL(db).query_db(query,data)
        return(user)
    

    @staticmethod
    def validate(data):
        is_valid = True
        for key in data:
            if len(str(data[key])) <= 0:
                flash('all fields are required and cannot be left blank', 'error1')
                is_valid = False
                break
        if len(data['username'])< 2:
            flash('username must have more than 2 characters')
            is_valid = False
        if len(data['password']) < 6:
            flash('password must be at least 6 characters long')
            is_valid = False
        if not REGEX_EMAIL.match(data['email']):
            flash('invalid email format')
            is_valid = False
        if not REGEX_PW_FORM.match(data['password']):
            flash('password must not contain spaces and must contain both alpha and numeric characters and at least one ! @ # $, or ? * symbol')
            is_valid = False
        if not data['password'] == data['confirm_password']:
            flash('password and confirm password do not match')
            is_valid = False
        if  User.getUserByEmail(data['email']):
            flash('that email is already registered to another account')
            is_valid = False
        return(is_valid)
    
    @staticmethod
    def validate_login(data):
        is_valid = True
        for key in data:
            if len(str(data[key])) <= 0:
                flash('all fields are required and cannot be left blank', 'error1')
                is_valid = False
                break
        user = User.getUserByEmail(data['email'])
        if user:
            if not bcrypt.check_password_hash(user.password, data['password']):
                flash("THATS IT! YOUR ARE A HACKER AND I AM CALLING THE POLICE THE PASSWORD DOESNT MATCH..or it was just a typo!!!")
                is_valid = False
        else:
            flash('information does not match an existing user')
            is_valid = False
        return(is_valid)