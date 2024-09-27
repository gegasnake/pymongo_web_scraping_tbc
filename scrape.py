from typing import Tuple, Any
import requests
from bs4 import BeautifulSoup
import aiohttp
import asyncio
from concurrent.futures import ThreadPoolExecutor
import certifi

WEBSITE = "https://kulinaria.ge/"
PRODUCT_COUNT = 10  # This is a constant defining the maximum number of products to parse.


async def fetch(session, url):
    """
    Fetch the content of a URL asynchronously.

    Args:
        session (aiohttp.ClientSession): The session object for making requests.
        url (str): The URL to fetch.

    Returns:
        str: The content of the response as text.
    """
    async with session.get(url, ssl=False) as response:
        return await response.text()


async def parse_main_category_page(session, main_url="https://kulinaria.ge/receptebi/cat/msoplio-samzareulo/"):
    """
    Parse the main category page to retrieve recipe URLs.

    Args:
        session (aiohttp.ClientSession): The session object for making requests.
        main_url (str): The URL of the main category page to parse. Default is a specific category.

    Returns:
        list: A list of recipe URLs found on the main category page.
    """
    response = await fetch(session, main_url)
    soup = BeautifulSoup(response, 'html.parser')

    recipe_urls = []
    recipe_url = soup.findAll("div", class_="box box--author kulinaria-col-3 box--massonry", limit=PRODUCT_COUNT)
    for url in recipe_url:
        found_url = url.find('a')["href"]
        recipe_urls.append(found_url)

    return recipe_urls


async def parse_recipe(session, url):
    """
    Parse a recipe page to extract detailed recipe information.

    Args:
        session (aiohttp.ClientSession): The session object for making requests.
        url (str): The URL of the recipe page to parse.

    Returns:
        dict: A dictionary containing recipe details, including name, image URL, author, steps, ingredients, and description.
    """
    response = await fetch(session, url)
    soup = BeautifulSoup(response, 'html.parser')

    # 1. Get recipe name
    recipe_name = soup.find('div', class_='post__title').find('h1').get_text(strip=True)

    # 2. Get recipe image URL
    image_url = soup.find('div', class_='post__img').find('img')['src']

    # 3. Get author name
    author_name = soup.find('div', class_='post__author').find('a').get_text(strip=True)

    # 4. Get recipe steps
    receipt_steps = soup.find('div', class_='lineList').find_all('div', class_='lineList__item')

    receipt = []
    for rec in receipt_steps:
        rec_text = rec.find('p').get_text(strip=True).replace('\r', '').replace('\n', '')
        receipt.append(rec_text)

    # 5. Get recipe ingredients
    ingredients_list = []
    ingredients_div = soup.find('div', class_='list')
    for ingredient_item in ingredients_div.find_all('div', {'class': 'list__item'}):
        ingredient_text = (ingredient_item.get_text(separator=' ', strip=True)
                           .replace('\n\xa0\n                            \n                            ', '')
                           .replace('\n                           ', ''))
        ingredients_list.append(ingredient_text)

    description = soup.find('div', class_='post__description').get_text(strip=True)

    dct = {
        "Recipe Name": recipe_name,
        "Recipe url": url,
        "Image url": image_url,
        "Author": author_name,
        "receipt": receipt,
        "ingredients": ingredients_list,
        "description": description
    }

    return dct


async def return_every_parse() -> tuple[Any]:
    """
    Retrieve and parse all recipes from the main category page.

    Returns:
        list: A list of dictionaries containing details of each recipe.
    """
    async with aiohttp.ClientSession() as session:
        list_of_urls = await parse_main_category_page(session)
        tasks = [parse_recipe(session, WEBSITE + url) for url in list_of_urls]
        list_of_information = await asyncio.gather(*tasks)
        return list_of_information


# Run the asynchronous function
if __name__ == "__main__":
    recipes = asyncio.run(return_every_parse())
    print(recipes)