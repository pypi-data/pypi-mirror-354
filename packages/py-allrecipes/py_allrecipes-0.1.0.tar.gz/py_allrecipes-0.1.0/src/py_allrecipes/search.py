import requests
from bs4 import BeautifulSoup
import re


def __get_search_url(query: str) -> str:
    """Constructs the search URL for Allrecipes."""
    return f"https://www.allrecipes.com/search?q={query}"


def search_recipes(query: str) -> list:
    """Searches for recipes on Allrecipes and returns a list of recipe titles, URLs, and ratings (if available)."""
    url = __get_search_url(query)
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    recipe_elements = soup.find_all(
        "a",
        class_="comp mntl-card-list-card--extendable mntl-universal-card mntl-document-card mntl-card card card--no-image",
    )

    recipes = []
    for element in recipe_elements:
        text = element.get_text(strip=True)
        # Extract href using regex from the string representation
        element_str = str(element)
        href_match = re.search(r'href=["\"](.*?)["\"]', element_str)
        link = href_match.group(1) if href_match else None
        # Try to split title and ratings
        if "Ratings" in text:
            parts = text.rsplit("Ratings", 1)
            title = parts[0].strip()
            ratings = None
            match = re.search(r"(\d+[\,\d]*)$", title)
            if match:
                ratings = int(match.group(1).replace(",", ""))
                title = title[: match.start()].strip()
        else:
            title = text
            ratings = None
        recipe = {"title": title, "url": link}
        if ratings is not None:
            recipe["ratings"] = ratings
        recipes.append(recipe)

    return recipes
