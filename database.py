import pymongo

class Database(object):
    # In order for all objects of class having the same uri, we are not putting it as a def __init__, but rather as a class or static variable:
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    # To tell python that we are not using the init method, adding @staticmethod:
    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['fullstack']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    # Retrurns cursor at the beginning of the collection
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    # Returns the first element in the collection
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)
