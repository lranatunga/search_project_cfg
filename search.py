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

def request():
    user_request = input("Enter an ingredient: ")
    result_recipes = search_recipe(user_request)
    #print(user_request)
    print(result_recipes)

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
    
request()
