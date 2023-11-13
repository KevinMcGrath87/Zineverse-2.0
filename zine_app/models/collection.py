from flask import flash
from zine_app.__init__ import app
from zine_app.config.mysqlconnection import connectToMySQL
from zine_app.config.utils import DATABASE


db = DATABASE

class Collection:
    def __init__(self, data):
        self.id = data['id']
        self.collection_name = data['collection_name']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.update_at = data['updated_at']

    def getZinesInCollection(self):
        query = 'SELECT * from zines LEFT JOIN collected on zines.id = collected.zine_id LEFT JOIN collections on collected.collection_id = collections.id WHERE collections.id =  %(id)s'
        data ={'id':self.id}
        result = connectToMySQL(db).query_db(query,data)
        return(result)




    @classmethod 
    def createNew(cls, user_id, collection_name):
        query = "INSERT into collections (collection_name, user_id, created_at, updated_at) VALUES (%(collection_name)s,%(user_id)s, NOW(),NOW())"
        data = {'user_id':user_id,'collection_name':collection_name}
        result = connectToMySQL(db).query_db(query,data)
        return(result)
    

    
        