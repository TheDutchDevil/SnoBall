from pymongo import MongoClient

class MongoDbConnector:

    def __init__(self, URL):
        self.url = URL
        self.client = MongoClient(URL)

    def insert_entry(self, database_name, collection_name, entry):
        collection = self.get_collection_for_database(database_name, collection_name)
        collection.insert_one(entry)

    def insert_entries(self, database_name, collection_name, entries):
        collection = self.get_collection_for_database(database_name, collection_name)
        collection.insert_many(entries)

    def find_entry(self, database_name, collection_name, query):
        collection = self.get_collection_for_database(database_name, collection_name)
        return collection.find_one(query)

    def find_entries(self, database_name, collection_name, query):
        collection = self.get_collection_for_database(database_name, collection_name)
        return collection.find_many(query)

    def get_all_entries(self, database_name, collection_name):
        collection = self.get_collection_for_database(database_name, collection_name)
        return list(collection.find({}, {'_id': False}))

    def get_collection_for_database(self, database_name, collection_name):
        return self.client[database_name].collection[collection_name]

    def delete_collection(self, database_name, collection_name):
        self.client[database_name].drop_collection(collection_name)