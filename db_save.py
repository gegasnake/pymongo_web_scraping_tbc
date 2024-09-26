import pymongo



def main():
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    my_db = client["mydatabase"]

    my_collection = my_db["customers"]
    my_collection.delete_many({})

    my_data = {"name": "John", "address": "Highway 37"}
    my_collection.insert_one(my_data)

    for doc in my_collection.find():
        print(doc)

if __name__=="__main__":
    main()