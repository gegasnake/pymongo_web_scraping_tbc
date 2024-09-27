from db_save import DataManager
from scrape import return_every_parse
import asyncio


def main():
    uri = "mongodb://localhost:27017/"
    data_name = "mydatabase"
    collection_name = "recipes"
    data_manager = DataManager(uri=uri, data_name=data_name, collection_name=collection_name)

    recipes = asyncio.run(return_every_parse())

    try:
        data_manager.save_data(recipes)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
