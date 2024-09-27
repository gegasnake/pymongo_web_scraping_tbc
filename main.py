from data_analyze import DataAnalyzer
from db_save import DataSave
from scrape import return_every_parse
import asyncio


def main():
    uri = "mongodb://localhost:27017/"
    data_name = "mydatabase"
    collection_name = "recipes"

    data_save = DataSave(uri=uri, data_name=data_name, collection_name=collection_name)
    data_save.clear_collection()

    recipes = asyncio.run(return_every_parse())

    try:
        data_save.save_data(recipes)
    except Exception as e:
        print(f"An error occurred: {e}")

    data_analyzer= DataAnalyzer(data_save.collection)
    data_analyzer.author_with_most_recipes()
    print("#####################################")
    data_analyzer.average_ingredients_per_recipe()
    print("#####################################")
    data_analyzer.average_receipt_per_recipe()

if __name__ == '__main__':
    main()
