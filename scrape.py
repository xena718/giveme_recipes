
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
     


def get_recipe_from_url(url, recipe_courses, recipe_cuisine,recipe_specialdiets):
    """return a recipe with formats complying to my yummy recipe app"""
    html_doc = requests.get(url).content
    soup = BeautifulSoup(html_doc, 'html.parser')

    recipe_container = soup.find("div", {"class": "js-ad-section"})

    title = recipe_container.find('h1').get_text().strip() # a string 
    if recipe_container.find("div", {"class": "ChfBy_lnk"}):
        author = recipe_container.find("div", {"class": "ChfBy_lnk"}).get_text().strip()
        if author == "":
            author = "Chengfeng"
    else:
        author = "Chengfeng"
    description = recipe_container.find("p", {"class": "tab_crl"}).get_text().strip()
    photo_url = recipe_container.find('div', {'class': 'img-gr'}).img['src']
    if recipe_container.find("span", text="Recipe Servings"):
        servings_str = recipe_container.find("span", text="Recipe Servings").next_sibling.get_text().strip()
        servings = int(servings_str)
    else:
        servings = 2
    
    if recipe_container.find("span", text="Prep Time"):
        prep_time = recipe_container.find("span", text="Prep Time").next_sibling.get_text().strip()
    else: 
        prep_time = "10 min"
    if recipe_container.find("span", text="Cook Time"): 
        cook_time = recipe_container.find("span", text="Cook Time").next_sibling.get_text().strip()
    else:
        cook_time = "20 min"
    # ingredients
    recipe_ingredients = recipe_container.find('ul', {"class": "RcpIngd-tp_ul"})
    # ingredients1 = [x.get_text().strip() for x in recipe_ingredients.find_all('li')]
    ingredients =[]
    for line in recipe_ingredients.find_all("li"):
        if not line.find("b"):
            line_text = line.get_text().strip()
            if line_text[-1] != ":":
                ingredients.append(line_text)

    recipe_ingredients = []
    for ingredient in ingredients:
        recipe_ingredient= {}
        items_ls = ingredient.split(" ")
        # print(items_ls)

        # if isinstance(int(items_ls[0][0]), int): #this means the first item in the list is the quantity string.
        if items_ls[0].lower() != "for":
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


def get_recipes_from_urls_set1():
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
        recipe_courses = ["Main Dish","Lunch"]
        recipe_cuisine = "Indian"
        recipe_specialdiets = ["Non-Vegetarian"]
        recipe_from_url = get_recipe_from_url(url, recipe_courses, recipe_cuisine,recipe_specialdiets)
        write_json(recipe_from_url, filename='recipes_ndtv.json')

def get_recipes_from_urls_set2():
    url1 = "https://food.ndtv.com/recipe-mango-phalsa-chaat-957000"
    url2 = "https://food.ndtv.com/recipe-no-oven-garlic-bread-956904"
    url3 = "https://food.ndtv.com/recipe-chicken-doughnuts-956620"
    url4 = "https://food.ndtv.com/recipe-protein-balls-956572"
    url5 = "https://food.ndtv.com/recipe-chicken-and-baby-spinach-kebab-956562"

    urls = [url1,url2,url3,url4,url5]
    for url in urls:
        recipe_courses = ["Appetizer & Snacks"]
        recipe_cuisine = "Mediterranean"
        recipe_specialdiets = ["Vegetarian","Gluten-free"]
        recipe_from_url = get_recipe_from_url(url, recipe_courses, recipe_cuisine,recipe_specialdiets)
        write_json(recipe_from_url, filename='recipes_ndtv.json')
# get_recipes_from_urls_set2()

def get_recipes_from_urls_set3():
    url1 = "https://food.ndtv.com/recipe-golden-coin-eggs-957103"
    url2 = "https://food.ndtv.com/recipe-eggs-benedict-with-sesame-bagels-956935"
    url3 = "https://food.ndtv.com/recipe-chilli-garlic-omelette-956606"
    url4 = "https://food.ndtv.com/recipe-homemade-veg-grilled-sandwich-956277"
    url5 = "https://food.ndtv.com/recipe-green-onion-and-mushroom-omelette-956206"

    urls = [url1,url2,url3,url4,url5]
    for url in urls:
        recipe_courses = ["Breakfast & Brunch"]
        recipe_cuisine = "American"
        recipe_specialdiets = ["Vegetarian","Gluten-free"]
        recipe_from_url = get_recipe_from_url(url, recipe_courses, recipe_cuisine,recipe_specialdiets)
        write_json(recipe_from_url, filename='recipes_ndtv.json')

# get_recipes_from_urls_set3()

def get_recipes_from_urls_set4():
    url1 = "https://food.ndtv.com/recipe-scotch-egg-and-broth-778615"
    url2 = "https://food.ndtv.com/recipe-buttermilk-scones-263274"
    url3 = "https://food.ndtv.com/recipe-pears-in-saffron-and-rose-syrup-219671"
    url4 = "https://food.ndtv.com/recipe-pound-cake-219672"
    url5 = "https://food.ndtv.com/recipe-tartare-sauce-continental-219782"

    urls = [url1,url2,url3,url4,url5]
    for url in urls:
        recipe_courses = ["Appetizer & Snacks","Side Dishes","Breakfast & Brunch"]
        recipe_cuisine = "British"
        recipe_specialdiets = ["Vegetarian"]
        recipe_from_url = get_recipe_from_url(url, recipe_courses, recipe_cuisine,recipe_specialdiets)
        write_json(recipe_from_url, filename='recipes_ndtv.json')

# get_recipes_from_urls_set4()

def get_recipes_from_urls_set5():
    url1 = "https://food.ndtv.com/recipe-caribbean-rice-salad-264277"

    urls = [url1]
    for url in urls:
        recipe_courses = ["Side Dishes","Salad"]
        recipe_cuisine = "Caribbean"
        recipe_specialdiets = ["Vegetarian"]
        recipe_from_url = get_recipe_from_url(url, recipe_courses, recipe_cuisine,recipe_specialdiets)
        write_json(recipe_from_url, filename='recipes_ndtv.json')

# get_recipes_from_urls_set5()


def get_recipes_from_urls_set6():
    url1 = "https://food.ndtv.com/recipe-chicken-chilli-gravy-957039"
    url2 = "https://food.ndtv.com/recipe-mushroom-noodles-956754"
    url3 = "https://food.ndtv.com/recipe-sheng-jian-bao-955054"
    url4 = "https://food.ndtv.com/recipe-stuffed-eggplant-with-schezwan-sauce-953402"
    url5 = "https://food.ndtv.com/recipe-mapo-tofu-with-spring-onion-and-black-beans-874405"

    urls = [url1,url2,url3,url4,url5]
    for url in urls:
        recipe_courses = ["Lunch", "Main Dish"]
        recipe_cuisine = "Chinese"
        recipe_specialdiets = ["Non-Vegetarian"]
        recipe_from_url = get_recipe_from_url(url, recipe_courses, recipe_cuisine,recipe_specialdiets)
        write_json(recipe_from_url, filename='recipes_ndtv.json')

# get_recipes_from_urls_set6()


def get_recipes_from_urls_set7():
    url1 = "https://food.ndtv.com/recipe-algerienne-fish-559503"
    url2 = "https://food.ndtv.com/recipe-pea-soup-french-1-484994"
    url3 = "https://food.ndtv.com/recipe-low-fat-french-onion-soup-211671"
    url4 = "https://food.ndtv.com/recipe-coq-au-vin-106758"
    url5 = "https://food.ndtv.com/recipe-french-onion-soup-with-cheese-souffle-100380"

    urls = [url1,url2,url3,url4,url5]
    for url in urls:
        recipe_courses = ["Soups & Stews"]
        recipe_cuisine = "French"
        recipe_specialdiets = ["Non-Vegetarian"]
        recipe_from_url = get_recipe_from_url(url, recipe_courses, recipe_cuisine,recipe_specialdiets)
        write_json(recipe_from_url, filename='recipes_ndtv.json')
# get_recipes_from_urls_set7()

def get_recipes_from_urls_set8():
    url1 = "https://food.ndtv.com/recipe-fenugreek-and-lal-maat-crostini-143104"
    url2 = "https://food.ndtv.com/recipe-methi-and-lotus-root-salad-fenugreek-lotus-root-salad-219111"
    url3 = "https://food.ndtv.com/recipe-greek-salad-1-572874"


    urls = [url1,url2,url3]
    for url in urls:
        recipe_courses = ["Side Dishes","Salad"]
        recipe_cuisine = "Greek"
        recipe_specialdiets = ["Vegetarian"]
        recipe_from_url = get_recipe_from_url(url, recipe_courses, recipe_cuisine,recipe_specialdiets)
        write_json(recipe_from_url, filename='recipes_ndtv.json')


# get_recipes_from_urls_set8()

def get_recipes_from_urls_set9():
    url1 = "https://food.ndtv.com/recipe-classic-pasta-amatriciana-954420"
    url2 = "https://food.ndtv.com/recipe-fettuccine-pomodoro-952523"
    url3 = "https://food.ndtv.com/recipe-lemon-chicken-and-rocket-pasta-844892"
    url4 = "https://food.ndtv.com/recipe-pizza-panne-576702"

    urls = [url1,url2,url3,url4]
    for url in urls:
        recipe_courses = ["Main Dish"]
        recipe_cuisine = "Italian"
        recipe_specialdiets = ["Non-Vegetarian"]
        recipe_from_url = get_recipe_from_url(url, recipe_courses, recipe_cuisine,recipe_specialdiets)
        write_json(recipe_from_url, filename='recipes_ndtv.json')

# get_recipes_from_urls_set9()


def get_recipes_from_urls_set10():
    url1 = "https://food.ndtv.com/recipe-chicken-balls-in-yakitori-sauce-349190"
    url2 = "https://food.ndtv.com/recipe-japanese-soba-noodles-753302"
    url3 = "https://food.ndtv.com/recipe-mediterranean-watermelon-salad-507291"
    url4 = "https://food.ndtv.com/recipe-pasta-with-roasted-mediterranean-veggies-328278"
    url5 = "https://food.ndtv.com/recipe-jowar-tacos-with-spicy-chicken-filling-735315"
    url6 = "https://food.ndtv.com/recipe-chicken-tagine-with-olives-and-preserved-lemons-955315"
    url7 = "https://food.ndtv.com/recipe-spanish-valencia-prawns-727527"
    url8 = "https://food.ndtv.com/recipe-young-jackfruit-and-water-chestnut-thai-red-curry-952395"
    url9 = "https://food.ndtv.com/recipe-turkish-tulumba-951354"
    url10 = "https://food.ndtv.com/recipe-vietnamese-cold-spring-rolls-291573"
    url11 = "https://food.ndtv.com/recipe-schezwan-paneer-955275"
    url12 = "https://food.ndtv.com/recipe-simrana-g-t-recipe-956986"
    url13 = "https://food.ndtv.com/recipe-thandai-macaron-956571"


    urls_Japanese = [url1,url2]
    for url in urls_Japanese:
        recipe_courses = ["Main Dish"]
        recipe_cuisine = "Japanese"
        recipe_specialdiets = ["Non-Vegetarian"]
        recipe_from_url = get_recipe_from_url(url, recipe_courses, recipe_cuisine,recipe_specialdiets)
        write_json(recipe_from_url, filename='recipes_ndtv.json')
    urls_Mediterranean = [url3,url4]
    for url in urls_Mediterranean:
        recipe_courses = ["Salad"]
        recipe_cuisine = "Mediterranean"
        recipe_specialdiets = ["Vegetarian"]
        recipe_from_url = get_recipe_from_url(url, recipe_courses, recipe_cuisine,recipe_specialdiets)
        write_json(recipe_from_url, filename='recipes_ndtv.json')
    urls_Mexican = [url5]
    for url in urls_Mexican:
        recipe_courses = ["Main Dish"]
        recipe_cuisine = "Mexican"
        recipe_specialdiets = ["Non-Vegetarian"]
        recipe_from_url = get_recipe_from_url(url, recipe_courses, recipe_cuisine,recipe_specialdiets)
        write_json(recipe_from_url, filename='recipes_ndtv.json')
    urls_Moroccan = [url6]
    for url in urls_Moroccan:
        recipe_courses = ["Main Dish"]
        recipe_cuisine = "Moroccan"
        recipe_specialdiets = ["Non-Vegetarian"]
        recipe_from_url = get_recipe_from_url(url, recipe_courses, recipe_cuisine,recipe_specialdiets)
        write_json(recipe_from_url, filename='recipes_ndtv.json')

    urls_Spanish = [url7]
    for url in urls_Spanish:
        recipe_courses = ["Main Dish"]
        recipe_cuisine = "Spanish"
        recipe_specialdiets = ["Non-Vegetarian"]
        recipe_from_url = get_recipe_from_url(url, recipe_courses, recipe_cuisine,recipe_specialdiets)
        write_json(recipe_from_url, filename='recipes_ndtv.json')
    
    urls_Thai = [url8]
    for url in urls_Thai:
        recipe_courses = ["Main Dish"]
        recipe_cuisine = "Thai"
        recipe_specialdiets = ["Non-Vegetarian"]
        recipe_from_url = get_recipe_from_url(url, recipe_courses, recipe_cuisine,recipe_specialdiets)
        write_json(recipe_from_url, filename='recipes_ndtv.json')

    urls_Turkish = [url9]
    for url in urls_Turkish:
        recipe_courses = ["Side Dishes"]
        recipe_cuisine = "Turkish"
        recipe_specialdiets = ["Vegetarian","Gluten-free"]
        recipe_from_url = get_recipe_from_url(url, recipe_courses, recipe_cuisine,recipe_specialdiets)
        write_json(recipe_from_url, filename='recipes_ndtv.json')

    urls_Vietnamese = [url10]
    for url in urls_Vietnamese:
        recipe_courses = ["Side Dishes"]
        recipe_cuisine = "Vietnamese"
        recipe_specialdiets = ["Vegetarian","Gluten-free"]
        recipe_from_url = get_recipe_from_url(url, recipe_courses, recipe_cuisine,recipe_specialdiets)
        write_json(recipe_from_url, filename='recipes_ndtv.json')

    urls_Fusion = [url11]
    for url in urls_Fusion:
        recipe_courses = ["Main Dish"]
        recipe_cuisine = "Food Fusion"
        recipe_specialdiets = ["Non-Vegetarian"]
        recipe_from_url = get_recipe_from_url(url, recipe_courses, recipe_cuisine,recipe_specialdiets)
        write_json(recipe_from_url, filename='recipes_ndtv.json')

    urls_Others = [url12]
    for url in urls_Others:
        recipe_courses = ["Drink"]
        recipe_cuisine = "Others"
        recipe_specialdiets = ["Others"]
        recipe_from_url = get_recipe_from_url(url, recipe_courses, recipe_cuisine,recipe_specialdiets)
        write_json(recipe_from_url, filename='recipes_ndtv.json')

    urls_French = [url13]
    for url in urls_French:
        recipe_courses = ["Dessert"]
        recipe_cuisine = "French"
        recipe_specialdiets = ["Vegetarian"]
        recipe_from_url = get_recipe_from_url(url, recipe_courses, recipe_cuisine,recipe_specialdiets)
        write_json(recipe_from_url, filename='recipes_ndtv.json')



get_recipes_from_urls_set1()
get_recipes_from_urls_set2()
get_recipes_from_urls_set3()
get_recipes_from_urls_set4()
get_recipes_from_urls_set5()
get_recipes_from_urls_set6()
get_recipes_from_urls_set7()
get_recipes_from_urls_set8()
get_recipes_from_urls_set9()
get_recipes_from_urls_set10()



def get_recipes_from_urls_set_template():
    url1 = ""
    url2 = ""
    url3 = ""
    url4 = ""
    url5 = ""

    urls = [url1,url2,url3,url4,url5]
    for url in urls:
        recipe_courses = ["Appetizer & Snacks","Side Dishes","Breakfast & Brunch"]
        recipe_cuisine = "British"
        recipe_specialdiets = ["Vegetarian"]
        recipe_from_url = get_recipe_from_url(url, recipe_courses, recipe_cuisine,recipe_specialdiets)
        write_json(recipe_from_url, filename='recipes_ndtv.json')



# recipe_courses = ["Main Dish","Lunch"]
# recipe_cuisine = "Indian"
# recipe_specialdiets = ["Non-Vegetarian"]
# recipes_ndtv = []
# recipe_from_url9=get_recipe_from_url(url, recipe_courses, recipe_cuisine,recipe_specialdiets)
# recipes_ndtv.append(recipe_from_url9)
# print(recipes_ndtv)

