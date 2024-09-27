from idlelib.editor import darwin

from data_analyze import DataAnalyzer
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

    data_analyzer= DataAnalyzer(data_manager.collection)
    data_analyzer.author_with_most_recipes()
    print("#####################################")
    data_analyzer.average_ingredients_per_recipe()
    print("#####################################")
    data_analyzer.average_receipt_per_recipe()

if __name__ == '__main__':
    main()
