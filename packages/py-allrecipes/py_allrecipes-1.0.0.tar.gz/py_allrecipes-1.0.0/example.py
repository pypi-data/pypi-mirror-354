import py_allrecipes

url = py_allrecipes.search_recipes("chocolate cake")[1]["url"]
recipe = py_allrecipes.get_recipe(url)

print(recipe)
