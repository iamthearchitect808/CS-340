from pymongo import MongoClient
from pymongo import results
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson.json_util import loads
import json

class AnimalShelter(object):
    """CRUD operations for Animal collection in MongoDB"""
       
    def __init__(self, username: str, password: str):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        # Default authorization is for AAC database.
        self.client = MongoClient('mongodb://%s:%s@localhost:43325/?authSource=AAC' 
                                  % (username, password))
        self.database = self.client['AAC']
        
    def count_docs(self, collection):
        # For testing purposes.
        if collection is not None:
            return self.database.animals.find().count()
        else:
            raise Exception("Nothing to count")
            
    def count_query(self, collection, query):
        # For testing purposes.
        if collection is not None and query is not None:
            return self.database.animals.find(query).count()
        else:
            raise Exception("Nothing to count")
        
    def create(self, data):
        # the data should be a dictionary
        if data is not None:
            try:
                create_result = self.database.animals.insert_one(data) 
                if create_result.acknowledged:
                    return True
            except pymongo.errors.OperationFailure as err:
                print("Insert operation failed. Error:", str(err))
            except Exception as err:
                print("Something went wrong. Error:", str(err))
            return False
        
    def read(self, query):
        # the query should be a dictionary
        if query is not None:
            try:
                read_result = self.database.animals.find(query) 
                return read_result
            except pymongo.errors.TypeError as err:
                print("Query parameter is not a dictionary. Error: ", str(err))
            except Exception as err:
                print("Something went wrong. Error:", str(err))
            
    def update(self, update_query, desired_update, data_update):
        # the update query and data update should be dictionaries
        if data_update is not None:
            try:
                update_result = self.database.animals.update_many(update_query, data_update) 
                # initilize query to find documents after update:
                updated = self.database.animals.find(desired_update)
                # put results in a list:
                list_updated = list(updated)
                # format result list as json:
                json_data = dumps(list_updated, indent = 2)
                return json_data
            except Exception as err:
                print("Something went wrong. Error: ", str(err))
    
    def delete(self, delete_query):
        # the delete query should be a dictionary
        if delete_query is not None:
            try:
                delete_result = self.database.animals.delete_many(delete_query)
                # initialize query to find documents after delete:
                updated = self.database.animals.find(delete_query)
                # put results in a list
                deleted_list = list(updated)
                # format result list as json:
                json_data = dumps(deleted_list, indent = 2)
                return json_data
            except Exception as err:
                print("Something went wrong. Error: ", str(err))
                
            
    
            