class DataAnalyzer:

    def __init__(self, collection):
        self.__collection = collection

    def average_ingredients_per_recipe(self):
        try:

            pipeline = [
                {
                    '$project': {
                        'Recipe Name': 1,
                        'ingredients_count': {'$size': {'$ifNull': ['$ingredients', []]}}
                    }
                }
            ]

            result = list(self.__collection.aggregate(pipeline))

            if result:
                for recipe in result:
                    recipe_name = recipe.get('Recipe Name', 'Unknown')
                    ingredients_count = recipe.get('ingredients_count', 0)
                    print(f"Recipe: {recipe_name} ---> Ingredients count: {ingredients_count}")
            else:
                print("No data found")

        except Exception as e:
            print(f"An error occurred: {e}")

    def average_receipt_per_recipe(self):
        try:

            pipeline = [
                {
                    '$project': {
                        'Recipe Name': 1,
                        'receipt_count': {'$size': {'$ifNull': ['$receipt', []]}}
                    }
                }
            ]

            result = list(self.__collection.aggregate(pipeline))

            if result:
                for recipe in result:
                    recipe_name = recipe.get('Recipe Name', 'Unknown')
                    ingredients_count = recipe.get('receipt_count', 0)
                    print(f"Recipe: {recipe_name} ---> receipt_count count: {ingredients_count}")
            else:
                print("No data found")

        except Exception as e:
            print(f"An error occurred: {e}")

    def author_with_most_recipes(self):
        try:
            pipeline = [
                {
                    '$group': {
                        '_id': '$Author',
                        'recipe_count': {'$sum': 1}
                    }
                },
                {
                    '$sort': {'recipe_count': -1}
                },
                {
                    '$limit': 1
                }
            ]


            result = list(self.__collection.aggregate(pipeline))


            if result:
                print(f"Author: {result[0]['_id']}, Number of Recipes: {result[0]['recipe_count']}")
            else:
                print("No authors found.")

        except Exception as e:
            print(f"An error occurred: {e}")
