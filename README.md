# Recipe Scraping Project - kulinaria.ge

## Project Overview

This project is designed to scrape recipe data from the website [kulinaria.ge](https://kulinaria.ge), specifically targeting a category assigned to each team. The goal is to extract relevant information about each recipe and store it in a MongoDB database. Each team will be responsible for scraping recipes from their assigned category.

## Team Workflow

1. **Create a Repository**: Start by creating a new repository and invite your team members.
2. **Task Planning**: Divide the tasks from the assignment among the team members. Use a project management tool if necessary.
3. **Collaboration**: Stay in contact with your team regularly and share updates. Work together on complex issues if needed.
4. **Problem-Solving**: Reach out to the instructor for assistance if you encounter significant roadblocks.
5. **Teamwork Concerns**: If any team member is not cooperating, you may report it privately to the instructor.

## Task Requirements

Your team is responsible for scraping recipes from a specific category and storing the following information for each recipe:

- Recipe name
- Recipe URL
- Main category (e.g., `{title: სალათები, url: https://kulinaria.ge/receptebi/cat/salaTebi/}`)
- Subcategory (e.g., `{title: ცხელი სალათები, url: https://kulinaria.ge/receptebi/cat/salaTebi/cxeli-salaTebi/}`)
- Main image URL
- Short description
- Author name
- Number of servings
- Ingredients (as a list)
- Preparation steps (with step number and description)

## Code Explanation

### Scraping Logic

The project uses `aiohttp` for asynchronous requests to speed up the scraping process. We extract data from recipe pages using `BeautifulSoup`. The `asyncio` library is used to manage asynchronous tasks, allowing for efficient multi-page scraping.

### Example Scraping Code

```python
import requests
from bs4 import BeautifulSoup
import aiohttp
import asyncio
from concurrent.futures import ThreadPoolExecutor

WEBSITE = "https://kulinaria.ge/"
PRODUCT_COUNT = 10  # This is a constant defining the maximum number of products to parse.

async def fetch(session, url):
    """Fetch the content of a URL asynchronously."""
    async with session.get(url, ssl=False) as response:
        return await response.text()

async def parse_main_category_page(session, main_url="https://kulinaria.ge/receptebi/cat/msoplio-samzareulo/"):
    """Parse the main category page to retrieve recipe URLs."""
    response = await fetch(session, main_url)
    soup = BeautifulSoup(response, 'html.parser')

    recipe_urls = []
    recipe_url = soup.findAll("div", class_="box box--author kulinaria-col-3 box--massonry", limit=PRODUCT_COUNT)
    for url in recipe_url:
        found_url = url.find('a')["href"]
        recipe_urls.append(found_url)

    return recipe_urls

```

### Database Management and Analysis Logic

#### db_save.py

The `db_save.py` module is responsible for managing the connection to the MongoDB database and saving the scraped recipe data. It uses the `pymongo` library for database interactions and ensures that the collection is cleared before inserting new data to maintain a clean dataset.

**Key Components:**
- **DataManager Class**: This class encapsulates all database-related operations, including connecting to the database and saving scraped recipes.
- **Methods**:
  - `save_data`: Takes a list of recipe data and inserts it into the MongoDB collection.
  - `clear_collection`: Clears existing entries in the collection before inserting new data, preventing data duplication.

**Example Data Saving Code:**

```python
from pymongo import MongoClient

class DataManager:
    def __init__(self, db_name='recipe_db', collection_name='recipes'):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def clear_collection(self):
        """Clears the existing collection before new data insertion."""
        self.collection.delete_many({})

    def save_data(self, recipes):
        """Inserts the scraped recipe data into the MongoDB collection."""
        if recipes:
            self.collection.insert_many(recipes)

```
#### data_analyze.py

The `data_analyze.py` module focuses on analyzing the data stored in the MongoDB database. It provides insights into the scraped recipes, allowing users to understand patterns and trends within the data.

**Key Components:**
- **DataAnalyzer Class**: This class contains methods for various types of data analysis, such as calculating averages and finding the most prolific authors.
- **Methods**:
  - `average_ingredients_per_recipe`: Computes and prints the average number of ingredients across all recipes.
  - `average_steps_per_recipe`: Computes and prints the average number of steps per recipe.
  - `author_with_most_recipes`: Identifies and prints the author with the highest number of recipes in the database.

**Example Data Analysis Code:**

```python
class DataAnalyzer:
    def __init__(self, collection):
        self.collection = collection

    def average_ingredients_per_recipe(self):
        """Calculates and prints the average number of ingredients per recipe."""
        total_ingredients = 0
        total_recipes = self.collection.count_documents({})
        
        for recipe in self.collection.find():
            total_ingredients += len(recipe.get('ingredients', []))
        
        average = total_ingredients / total_recipes if total_recipes else 0
        print(f"Average ingredients per recipe: {average}")

    def average_steps_per_recipe(self):
        """Calculates and prints the average number of steps per recipe."""
        total_steps = 0
        total_recipes = self.collection.count_documents({})
        
        for recipe in self.collection.find():
            total_steps += len(recipe.get('steps', []))
        
        average = total_steps / total_recipes if total_recipes else 0
        print(f"Average steps per recipe: {average}")

    def author_with_most_recipes(self):
        """Prints the author with the most recipes."""
        author_counts = {}
        
        for recipe in self.collection.find():
            author = recipe.get('author', 'Unknown')
            author_counts[author] = author_counts.get(author, 0) + 1
        
        most_recipes_author = max(author_counts, key=author_counts.get, default='No authors found')
        print(f"Author with the most recipes: {most_recipes_author}")
```
## Running The project
1. install required dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the scraping process:
   ```
    python main.py
   ```
