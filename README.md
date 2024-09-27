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
## Running The project
1. install required dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the scraping process:
   ```
    python main.py
   ```
