from flask import flash
from zine_app.models.user import User
from zine_app.config.mysqlconnection import connectToMySQL
from zine_app.config.utils import UPLOAD_FOLDER, ALLOWED_EXTENSIONS,DATABASE
from werkzeug.utils import secure_filename
import os
db = DATABASE

class Zine:
    def __init__(self, data):
        self.id = data['id']
        self.author = data['author']
        self.title = data['title']
        self.description = data['description']
        self.pages = data['pages']
        self.likes = data['likes']
        self.path = data['path']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def update(self):
        data = self.__dict__
        query = 'UPDATE zines SET author = %(author)s, title = %(title)s, description = %(description)s, pages = %(pages)s, likes = %(likes)s, updated_at = NOW() WHERE zines.id = %(id)s '
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def getZine(cls, zine_id):
        query = 'SELECT * FROM zines WHERE zines.id = %(zine_id)s'
        data = {'zine_id':zine_id}
        result = connectToMySQL(db).query_db(query, data)
        return(cls(result[0]))


    @classmethod
    def save(cls,data,user_id):
        query = "INSERT INTO zines(title, author,path, description,pages, likes, created_at, updated_at, author_id) VALUES(%(title)s, %(author)s,%(path)s, %(description)s,%(pages)s,%(likes)s ,NOW(),NOW(),%(author_id)s)"
        data['author_id']= user_id
        result =connectToMySQL(db).query_db(query,data)
        # previous query should return the zine id
        # query to get zine id? query to get user id
        return(result)

    
    


    @classmethod
    def createZine(cls, data, id):
        if cls.validate_zine(data,id):
            path = os.path.join(UPLOAD_FOLDER, data['title']+'_'+str(id))
            print(path)
            data['path']=path
            data['pages']=0
            data['likes']=0
            os.mkdir(path)
            cls.save(data,id)
        else:
            return(False)
        


    @classmethod
    def upload(cls, file, zine_id):
        zine = cls.getZine(zine_id)
        filename = file.filename
        path = zine.path
        length = len(os.listdir(path))
        if file and cls.allowed_file(filename):
            namesplit = filename.rsplit('.',1)
            namesplit[0]=str(length)
            filename = namesplit[0] + '.' + namesplit[1]
            securedFilename = secure_filename(filename)
            print(f'saving to {path}')
            zine.pages = zine.pages + 1
            print(zine.__dict__)
            zine.update()
            file.save(os.path.join(path,securedFilename))
            return(True)
        else:
            flash('issues with file upload. likely an incorrect filetype.')
            return(False)


        





    # @classmethod
    # def get_by_user(cls, id):
    #     query = "SELECT * FROM zines WHERE zines.author_id = %(id)s"
    #     data = {'id':id}
    #     result = connectToMySQL(db).query_db(query,data)
    #     zines = []
    #     for zine in result:
    #         zines.append(Zine(result[zine]))
    #     return zines

    @classmethod
    def get_by_user(cls, id):
        query = 'SELECT * FROM users LEFT JOIN collections ON users.id = collections.user_id LEFT JOIN collected ON collections.id = collected.collection_id LEFT JOIN zines ON collected.zine_id = zines.id  WHERE users.id = %(id)s'
        data = {'id':id}
        result = connectToMySQL(db).query_db(query,data)
        currentUser = User(result[0])
        zines = [];
        for zine in result:
            zines.append(cls(zine))
        for zine in zines:
            currentUser.zines.append(zine)
        return zines


    @staticmethod
    def validate_zine(data,id):
        is_valid = True
        zineList = Zine.get_by_user(id)
        for zine in zineList:
            if data['title']== zine.title and data['author']== zine.author:
                flash('zine already in database')
                is_valid = False
            if not data['description']:
                flash("cannot have empty description")
                is_valid = False
            if not data['title']:
                flash('cannot have empty title')
                is_valid = False
            if not data['author']:
                flash('cannot have empty author')
                is_valid = False
        return(is_valid)


    @staticmethod
    def allowed_file(filename):
        if(filename == ''):
            flash('no file selected')
            return False
        return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS
