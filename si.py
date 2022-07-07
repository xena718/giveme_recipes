units=["tablespoons", "tablespoon", "T", "TB", "Tbl", "Tbsp", 
    "cups","cup","c","C",
    "teaspoons", "teaspoon", "t", "tsp", "tbsp",
    "pints","pint","pt",
    "oz","OZ","ounces","ounce",
    "milliliters","milliliter","ml","mL",
    "liters","liter","L",
    "pounds","pound","LB","lb",
    "a pinch","a dash",
    "gallons","gallon","gl","GL","Gal",
    "kilograms","kilogram","kg",
    "grams","gram","g", "gm", "gms",
    "","no unit","other unit", "inch","drops"]

ingredient_catogories = ["Baked and Bakery", "Beverages", "Canned Goods and Soups", "Herbs and Spices", "Meat and Seafood",  "Vegetables and Fruits",  "Dairy, Eggs and Cheese",  "Grains, Pasta, and Sides",  "Condiments and Seasonings",  "Basic Cooking Ingredients",  "Baking Supplies",  "Uncategorized"]

# print(type(str(soup)))
# if "Recipe Servings" in str(soup): 
#     print("True #############")  # true was returned


# safeway_category_url = 'https://www.safeway.com/shop/aisles/grains-pasta-sides/pasta-sauce.3132.html?sort=&page=1'
# safeway_html_doc = requests.get(safeway_category_url).content
# safeway_soup = BeautifulSoup(safeway_html_doc, 'html.parser')
# products_container = safeway_soup.find("div", {"class": "product-card-grid"})
# print(safeway_soup)
# product_title_containers = products_container.find_all("a",{"class":"product-title__name"})
# print(product_title_containers)
# if "pizza" in str(product_title_containers): 
#     print("True #############")  # true was returned


