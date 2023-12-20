import os
from dotenv import load_dotenv
import requests

load_dotenv()

def search_recipe(ingredient):
    app_id = os.getenv("API_ID")
    app_key = os.getenv("API_KEY")
    response = requests.get(f'https://api.edamam.com/search?q={ingredient}&app_id={app_id}&app_key={app_key}')
    search_data = response.json()
    result = search_data['hits']
    #print(result)
    return (result)

def save_recipe_to_file(recipe):
    with open('saved_recipes.txt', 'a') as recipe_file:
        recipe_file.write(f"Recipe: {recipe['label']}\n")
        recipe_file.write(f"URI: {recipe['uri']}\n")
        recipe_file.write(f"Meal Type: {recipe['mealType'][0]}\n")
        recipe_file.write(f"Dish Type: {recipe['dishType'][0]}\n")

        ingredients = recipe['ingredients']
        recipe_file.write("Ingredients:\n")
        for ingredient_info in ingredients:
            recipe_file.write(f"{ingredient_info['text']} {ingredient_info['quantity']}\n")

        instruction_lines = recipe.get('instructionLines', [])
        recipe_file.write("Instructions:\n")
        if instruction_lines:
            for instruction in instruction_lines:
                recipe_file.write(f" - {instruction}\n")
        else:
            recipe_file.write("No instruction lines available.\n")

        recipe_file.write("\n")

def request():
    user_request = input("Enter an ingredient: ")
    result_recipes = search_recipe(user_request)
    #print(user_request)
    #print(result_recipes)

    if not result_recipes:
        print(f"No recipes found for {user_request}.")
        return
    else:
        print(f"Recipes containing {user_request}")
        for result_recipe in result_recipes:
            recipe = result_recipe['recipe']
            print(recipe['label'])
            print(recipe['uri'])
            print(recipe['mealType'][0])
            print(recipe['dishType'][0])
            
            ingredients = recipe['ingredients']
            
            # Iterating through ingredients list
            for ingredient_info in ingredients:
                print(f"{ingredient_info['text']} {ingredient_info['quantity']}")
                #print(f"Quantity: {ingredient_info['quantity']}")
            
            instruction_lines = recipe.get('instructionLines', [])
            if instruction_lines:
                print("Instruction:")
                for instruction in instruction_lines:
                    print(f" - {instruction}")
            else:
                print("No instruction lines available.")
            
            save_recipe_to_file(recipe)
    
request()

