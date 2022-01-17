def print_recipe(recipe):
    """Pretty print recipe, which is a dictionary whose keys are
    ingredients and whose values are their corresponding amounts.
    """
    for k,v in recipe.items():
        print(f"{k}: {v}")

def read_recipe(recipe_file_name):
    """Read recipe file 'recipe_file_name', and return ingredients as a
    dictionary whose keys are ingredients and whose values are the
    corresponding amounts.
    """
    recipe = dict()
    with open(recipe_file_name, 'r') as file:
        for line in file:
            clean_line = line.strip()
            if clean_line == '':
                continue
            raw_ingredient, raw_quantity = clean_line.split(',')
            quantity = int(raw_quantity)
            ingredient = raw_ingredient.strip()
            recipe[ingredient] = quantity
        return recipe

def write_recipe(recipe, recipe_file_name):
    """Write recipe to a file named recipe_file_name."""
    with open(recipe_file_name, 'w') as file:
        for k,v in recipe.items():
            file.write(f'{k},{v}\n')

def read_fridge(fridge_file_name):
    """Read fridge file 'fridge_file_name', and return the ingredients
    held in the given fridge as an ingredient=amount dictionary.
    """
    fridge = dict()
    with open(fridge_file_name, 'r') as file:
        for line in file:
            clean_line = line.strip()
            if clean_line == '':
                continue
            raw_ingredient, raw_quantity = clean_line.split(',')
            quantity = int(raw_quantity)
            ingredient = raw_ingredient.strip()
            if ingredient in fridge:
                fridge[ingredient] += quantity
            else:
                fridge[ingredient] = quantity

        return fridge
             
def is_cookable(recipe_file_name, fridge_file_name):
    """Return True if the contents of the fridge named fridge_file_name
    are sufficient to cook the recipe named recipe_file_name.
    """
    recipe = read_recipe(recipe_file_name) 
    fridge = read_fridge(fridge_file_name)
    for k,v in recipe.items():
        if k in fridge and fridge[k] >= v:
            continue
        else:
            return False
    return True

def add_recipes(recipes):
    """Return a dictionary representing the sum of all of
    the recipe dictionaries in recipes.
    """
    final_recipe = dict()
    for recipe in recipes:
        for k,v in recipe.items():
            if k in final_recipe:
                final_recipe[k] += v
            else:
                final_recipe[k] = v
    return final_recipe

def create_shopping_list(recipe_file_names, fridge_file_name):
    """Return the shopping list (a dictionary of ingredients and
    amounts) needed to cook the recipes named in recipe_file_names,
    after the ingredients already present in the fridge named
    fridge_file_name have been used.
    """
    recipes = []
    fridge = read_fridge(fridge_file_name)
    for recipe_file_name in recipe_file_names:
        recipes.append(read_recipe(recipe_file_name))
    final_recipe = add_recipes(recipes)
    shop_list = dict()

    for k,v in final_recipe.items():
        if k not in fridge:
            shop_list[k] = v
        else:
            shop_list[k] = max(0, v - fridge[k])
            if shop_list[k] == 0:
                del shop_list[k]
    return shop_list

def read_market(market_file_name):
    market = dict()
    with open(market_file_name, 'r') as file:
        for line in file:
            clean_line = line.strip()
            if clean_line == '':
                continue
            raw_ingredient, raw_price = clean_line.split(',')
            price = int(raw_price)
            ingredient = raw_ingredient.strip()
            market[ingredient] = price 
        return market

def total_price(shopping_list, market_file_name):
    """Return the total price in millicents of the given shopping_list
    at the market named market_file_name.
    """
    market = read_market(market_file_name)
    cost = 0
    for k,v in shopping_list.items():
        cost += market[k] * v
    return cost

def find_cheapest(shopping_list, market_file_names):
    """Return the name of the market in market_file_names
    offering the lowest total price for the given shopping_list,
    together with the total price.
    """
    cheapest = ['', -1]
    for market_file_name in market_file_names:
        cost = total_price(shopping_list, market_file_name)
        if cheapest[1] == -1 or cost < cheapest[1]:
            cheapest[0], cheapest[1] = market_file_name, cost

    return (cheapest[0], cheapest[1])

def update_fridge(fridge_file_name, recipe_file_names, market_file_names, new_fridge_file_name):
    """Compute the shopping list for the given recipes after the
    ingredients in fridge fridge_file_name have been used; find the cheapest
    market; and write the new fridge contents to new_fridge_file_name.
    Print the shopping list, the cheapest market name, and the total
    amount to be spent at that market.
    """
    shopping_list = create_shopping_list(recipe_file_names, fridge_file_name)
    cheapest = find_cheapest(shopping_list ,market_file_names)
    fridge = read_fridge(fridge_file_name)
    print("Shopping list:")
    for k,v in shopping_list.items():
        print(f'{k}: {v}')
        if k in fridge:
            fridge[k] += v
        else:
            fridge[k] = v
    print(f"Market: {cheapest[0]}")
    print(f"Total cost: {cheapest[1]}")

    with open(new_fridge_file_name, 'w') as file:
        for k,v in fridge.items():
            file.write(f"{k},{v}\n")

def distributed_shopping_list(shopping_list, market_file_names):
    """Distribute shopping_list across the markets named in market_file_names
    to minimize the total cost.
    """
    min_price = dict()
    shopping_dict = dict()
    for market_file_name in market_file_names:
        shopping_dict[market_file_name] = dict()
        market = read_market(market_file_name)
        for k in shopping_list.keys():
            if k not in min_price or min_price[k][1] > market[k]:
                min_price[k] = [market_file_name, market[k]]
    for k,v in min_price.items():
        name = v[0]
        shopping_dict[name][k] = shopping_list[k]

    return shopping_dict 

