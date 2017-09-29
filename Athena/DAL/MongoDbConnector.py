from pymongo import MongoClient

class MongoDbConnector:

    def __init__(self, URL):
        self.url = URL
        self.client = MongoClient(URL)

    def insertEntry(self, database_name, collection_name, entry):
        collection = self.getCollectionForDatabase(database_name, collection_name)
        collection.insert_one(entry)

    def insertEntries(self, database_name, collection_name, entries):
        collection = self.getCollectionForDatabase(database_name, collection_name)
        collection.insert_many(entries)

    def findEntry(self, database_name, collection_name, query):
        collection = self.getCollectionForDatabase(database_name, collection_name)
        return collection.find_one(query)

    def findEntries(self, database_name, collection_name, query):
        collection = self.getCollectionForDatabase(database_name, collection_name)
        return collection.find_many(query)

    def getCollectionForDatabase(self, database_name, collection_name):
        return self.client[database_name].collection[collection_name]

    def deleteCollection(self, database_name, collection_name):
        self.client[database_name].drop_collection(collection_name)