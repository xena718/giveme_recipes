
from bs4 import BeautifulSoup
import requests
from si import units

import json


url = 'https://food.ndtv.com/recipe-chawal-ki-kheer-951891'

def write_json(new_data, filename='recipes_ndtv.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data.append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
 
    # python object to be appended
     

def get_recipe_from_url(url):
    """return a recipe with formats complying to my yummy recipe app"""
    html_doc = requests.get(url).content
    soup = BeautifulSoup(html_doc, 'html.parser')

    recipe_container = soup.find("div", {"class": "js-ad-section"})

    title = recipe_container.find('h1').get_text().strip() # a string 
    author = recipe_container.find("div", {"class": "ChfBy_lnk"}).get_text().strip()
    description = recipe_container.find("p", {"class": "tab_crl"}).get_text().strip()
    photo_url = recipe_container.find('div', {'class': 'img-gr'}).img['src']
    servings_str = recipe_container.find("span", text="Recipe Servings").next_sibling.get_text().strip()
    servings = int(servings_str)
    prep_time = recipe_container.find("span", text="Prep Time").next_sibling.get_text().strip()
    cook_time = recipe_container.find("span", text="Cook Time").next_sibling.get_text().strip()

    recipe_cuisine = "Indian"
    recipe_courses = ["Main Dish","Lunch"]
    recipe_specialdiets=["Non-Vegetarian"]

    # ingredients
    recipe_ingredients = recipe_container.find('ul', {"class": "RcpIngd-tp_ul"})
    # ingredients1 = [x.get_text().strip() for x in recipe_ingredients.find_all('li')]
    ingredients =[]
    for line in recipe_ingredients.find_all("li"):
        if not line.find("b"):
            line_text = line.get_text().strip()
            ingredients.append(line_text)

    recipe_ingredients = []
    for ingredient in ingredients:
        recipe_ingredient= {}
        items_ls = ingredient.split(" ")
        # print(items_ls)

        # if isinstance(int(items_ls[0][0]), int): #this means the first item in the list is the quantity string.
        if items_ls[0].isdigit() or items_ls[0][0].isdigit(): #this means the first item in the list is the quantity string.
            if "-" in items_ls[0]:
                recipe_ingredient["quantity"] = items_ls[0][0]
            else:
                recipe_ingredient["quantity"] = items_ls[0]
            if items_ls[1] !="" and items_ls[1][0].isdigit():# deal with 1 1/2 situation
                if items_ls[2].lower() in units:
                    recipe_ingredient["unit_name"] = items_ls[2].lower()
                    recipe_ingredient["name"] = " ".join(items_ls[3:])
                else:
                    recipe_ingredient["unit_name"] = ""
                    recipe_ingredient["name"] = " ".join(items_ls[2:])
            else:
                if items_ls[1].lower() in units:
                    recipe_ingredient["unit_name"] = items_ls[1].lower()
                    recipe_ingredient["name"] = " ".join(items_ls[2:])
                else:
                    recipe_ingredient["unit_name"] = ""
                    recipe_ingredient["name"] = " ".join(items_ls[1:])
        else: 
            recipe_ingredient["name"] = " ".join(items_ls[:])
            recipe_ingredient["unit_name"] =""
            recipe_ingredient["quantity"] = ""
        recipe_ingredient["category"]=""
        recipe_ingredients.append(recipe_ingredient)

    recipe_instructions = recipe_container.find('div', {"class": "RcHTM_ul"})

    recipe_directions = {}

    for step_num_and_instruction in recipe_instructions.find_all('div', {"class": "RcHTM_li"}):
        for step_num in step_num_and_instruction.find('span', {"class": "RcHTM_cnt"}):
            # step_num_s = step_num.get_text().strip()
            step_num_s = step_num.strip(".")  # string
            # print(type(step_num_s))

        for step_instruction in step_num_and_instruction.find('span', {"class": "RcHTM_li-tx"}):
            step_instruction_s = str(step_instruction.strip("\r\n.")) # string. strip() deals with edge cases...
            # print(type(step_instruction_s))
        recipe_directions[step_num_s] = step_instruction_s

    recipe_from_url ={}
    recipe_from_url["title"]=title
    recipe_from_url["author"]=author
    recipe_from_url["description"]=description
    recipe_from_url["photo_url"]=photo_url
    recipe_from_url["servings"]=servings
    recipe_from_url["prep_time"]=prep_time
    recipe_from_url["cook_time"]=cook_time
    recipe_from_url["recipe_directions"]=recipe_directions
    recipe_from_url["recipe_ingredients"]=recipe_ingredients
    recipe_from_url["recipe_cuisine"]=recipe_cuisine
    recipe_from_url["recipe_courses"]=recipe_courses
    recipe_from_url["recipe_specialdiets"]=recipe_specialdiets

    return recipe_from_url

url1 = "https://food.ndtv.com/recipe-rara-mutton-956489"
url2 = "https://food.ndtv.com/recipe-mutton-akbari-956272"
url3 ="https://food.ndtv.com/recipe-badam-gosht-korma-956275"
url4 ="https://food.ndtv.com/recipe-saag-gosht-956318"
url5 ="https://food.ndtv.com/recipe-lahori-mutton-karahi-956165"
url6 ="https://food.ndtv.com/recipe-keto-butter-chicken-955086"
url7 = "https://food.ndtv.com/recipe-nilgiri-turkey-korma-954442"
url8 ="https://food.ndtv.com/recipe-laal-maas-954388"
url9 = "https://food.ndtv.com/recipe-lauki-gosht-952362"
url10 = "https://food.ndtv.com/recipe-steamed-fish-in-banana-leaves-956934"

urls = [url1,url2,url3,url4,url5,url6,url7,url8,url9,url10]
for url in urls:
    recipe_from_url=get_recipe_from_url(url)
    write_json(recipe_from_url, filename='recipes_ndtv.json')

recipes_ndtv = []
recipe_from_url9=get_recipe_from_url(url9)
recipes_ndtv.append(recipe_from_url9)
print(recipes_ndtv)



