from pymongo import MongoClient


class DataSave:

    def __init__(self, *, uri, data_name, collection_name):
        self.__client = MongoClient(uri)
        self.__db = self.__client[data_name]
        self.__collection = self.__db[collection_name]

    @property
    def collection(self):
        return self.__collection;

    def save_data(self, data):
        try:
            result = self.__collection.insert_many(data)
            print(f"Inserted document IDs: {result.inserted_ids}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def clear_collection(self):
        self.collection.delete_many({})






