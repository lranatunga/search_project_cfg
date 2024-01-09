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
    with open('saved_recipes.txt', 'a', encoding='utf-8') as recipe_file:
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
            
            for ingredient_info in ingredients:
                print(f"{ingredient_info['text']} {ingredient_info['quantity']}")
                #print(f"Quantity: {ingredient_info['quantity']}")
            
            instruction_lines = recipe.get('instructionLines', [])
            if instruction_lines:
                print("Instruction:")
                for instruction in instruction_lines:
                    print(f" - {instruction}\n")
            else:
                print(f"No instruction lines available.\n")
            
            save_recipe_to_file(recipe)
    
request()

def get_recipe_details(requested_recipe):
    with open('saved_recipes.txt', 'r') as saved_recipe_file:
        found_recipe = False
        uri = None
        ingredients = []
        for line in saved_recipe_file:
            if "Recipe:" in line and requested_recipe in line:
                found_recipe = True
            elif found_recipe and "URI:" in line:
                uri = line.split("URI:")[1].strip()
                print(uri)
            elif found_recipe and "Ingredients:" in line:
                if line.strip() and not line.startswith("Instructions:"):
                    ingredients.append(line.strip())
                for ingredient_line in saved_recipe_file:
                    if ingredient_line.strip() and not ingredient_line.startswith(("Instructions:", "URI:")):
                        ingredients.append(ingredient_line.strip())
                    else:
                        break
                break

        return uri, ingredients

def nutrient_analys():
    app_id_nutrients = os.getenv("API_ID_NUTRITION")
    app_key_nutrients = os.getenv("API_KEY_NUTRITION")

    nutrient_analys_request = input("Do you want nutrient analysis? yes/no ").lower()

    if nutrient_analys_request == "yes":
        requested_recipe = input("Please enter recipe name: ").title()
        
        uri, ingredients = get_recipe_details(requested_recipe)
        print(uri)
        print(ingredients)

        if uri and ingredients:
            if not uri.startswith(("http://", "https://")):
                uri = "http://" + uri
            recipe_data = {
                "url": uri,
                "ingr": ingredients
            }

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            response_nutrient_analysis = requests.post(
                f"https://api.edamam.com/api/nutrition-details?app_id={app_id_nutrients}&app_key={app_key_nutrients}",
                headers=headers,
                json=recipe_data
            )

            recipe_nutrient_analysis = response_nutrient_analysis.json()
            print(recipe_nutrient_analysis)

            print(f"Calories: {recipe_nutrient_analysis['calories']} kcal")

            calories = recipe_nutrient_analysis['totalNutrients']['ENERC_KCAL']['quantity']
            calories_unit = recipe_nutrient_analysis['totalNutrients']['ENERC_KCAL']['unit']
            print(f"Total Calories: {calories} {calories_unit}")

            fat_quantity = recipe_nutrient_analysis['totalNutrients']['FAT']['quantity']
            fat_unit = recipe_nutrient_analysis['totalNutrients']['FAT']['unit']
            print(f"Total lipid (Fat): {fat_quantity} {fat_unit}")

            total_saturated = recipe_nutrient_analysis['totalNutrients']['FASAT']['quantity']
            total_saturated_unit = recipe_nutrient_analysis['totalNutrients']['FASAT']['unit']
            print(f"Total Saturated Fatty Acid: {total_saturated} {total_saturated_unit}")

            total_trans = recipe_nutrient_analysis['totalNutrients']['FATRN']['quantity']
            total_trans_unit = recipe_nutrient_analysis['totalNutrients']['FATRN']['unit']
            print(f"Total Trans Fatty Acid: {total_trans} {total_trans_unit}")

            total_mono = recipe_nutrient_analysis['totalNutrients']['FAMS']['quantity']
            total_mono_unit = recipe_nutrient_analysis['totalNutrients']['FAMS']['unit']
            print(f"Total Mono-saturated Fatty Acid: {total_mono} {total_mono_unit}")

            print("\n Thanks for searching recipes with us")
        else:
            print("Requested recipe not found in the saved file.")
    else:
        print("Thanks for searching recipes with us")

nutrient_analys()

