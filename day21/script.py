import sys; sys.path.append('../common')
import mylib as utils # pylint: disable=import-error

import re
from itertools import product
from collections import namedtuple, OrderedDict

# Read args
filename = 'input.txt' if len(sys.argv) == 1 else sys.argv[1]
print(filename, '\n')

###########################
# region COMMON

# To read food list ingredients and allergens
FOOD_REGEX = re.compile(r'^(.+) \(contains (.+)\)$')

# Combination of ingredient x allergen
FoodPair = namedtuple('FoodPair', ['ingredient', 'allergen'])

class FoodItem():
    def __init__(self, ingredients: set, allergens: set):
        self.ingredients = ingredients
        self.allergens = allergens

        # All ingredient x allergen pairs
        self.foodPairs = [FoodPair(i, a) for i, a in product(self.ingredients, self.allergens)]

def readFoodList(foodList: list) -> (list, set, set):
    foodItems = list()
    ingredients = set()
    allergens = set()
    for foodItem in foodList:
        # Parsing food item
        (ingredientsString, allergensString) = FOOD_REGEX.search(foodItem).group(1,2)
        foodItemIngredients = ingredientsString.split(' ')
        foodItemAllergens = allergensString.split(', ')

        # Adding food item
        foodItems.append(FoodItem(foodItemIngredients, foodItemAllergens))

        # Updating list of ingredients and allergens
        ingredients.update(foodItemIngredients)
        allergens.update(foodItemAllergens)

    return foodItems, ingredients, allergens

def findNonAllergenIngredients(foodItems: list, ingredients: set, allergens: set) -> (set, dict):
    # Get possible allergens for each ingredient
    ingredientPossibleAllergens = { ingredient: set() for ingredient in ingredients }
    for foodItem in foodItems:
        for foodPair in foodItem.foodPairs:
            ingredientPossibleAllergens[foodPair.ingredient].add(foodPair.allergen)

    # Search for all ingredients with no possible "listed" allergens
    nonAllergenIngredients = set()
    for ingredient in list(ingredients):
        # Remove all invalid possible allergens
        for allergen in set(ingredientPossibleAllergens[ingredient]):
            # If ingredient is an allergen, it must be in all other food item with this listed allergen
            if not all(ingredient in foodItem.ingredients for foodItem in foodItems if allergen in foodItem.allergens):
                ingredientPossibleAllergens[ingredient].remove(allergen)

        if len(ingredientPossibleAllergens[ingredient]) == 0:
            # Ingredient cannot possibly be an allergen
            ingredientPossibleAllergens.pop(ingredient)
            nonAllergenIngredients.add(ingredient)

    return nonAllergenIngredients, ingredientPossibleAllergens

def identityAllergens(ingredientPossibleAllergens: dict) -> OrderedDict:
    allergenIngredients = {}
    nbAllergens = len(ingredientPossibleAllergens.keys())
    while len(allergenIngredients.keys()) < nbAllergens:
        # Identify all ingredients with only one possible remaining allergen
        for ingredient, allergens in ingredientPossibleAllergens.items():
            unknownAllergens = [a for a in allergens if a not in allergenIngredients]
            if len(unknownAllergens) == 1:
                allergen = unknownAllergens[0]
                allergenIngredients[allergen] = ingredient

    return OrderedDict(sorted(allergenIngredients.items(), key=lambda item: item[0])) # Sorted by allergen

# endregion COMMON
###########################

###########################
# FETCH DATA
###########################
foodList = utils.readFileLines(filename)

(foodItems, ingredients, allergens) = readFoodList(foodList)
print('Number of listed food items: %d' % len(foodItems))
print('Number of unique ingredients: %d' % len(ingredients))
print('Number of unique listed allergens: %d\n' % len(allergens))

########
# PART 1
########

(nonAllergenIngredients, ingredientPossibleAllergens) = findNonAllergenIngredients(foodItems, ingredients, allergens)
nbAllergenIngredients = (len(ingredients) - len(nonAllergenIngredients))
total = len([foodItem for ingredient in nonAllergenIngredients for foodItem in foodItems if ingredient in foodItem.ingredients])

print('Number of ingredients with possible allergens: %d' % nbAllergenIngredients)
print('---------------------------------------------------------------------------------')
print('\n'.join(['%-10s --> %s' % (ingredient, allergens) for ingredient, allergens in ingredientPossibleAllergens.items()]))
print('---------------------------------------------------------------------------------')
print('Number of non allergen ingredients: %d\n' % len(nonAllergenIngredients))
print('1) Number of time non allergen ingredients are listed in all food items: %d\n' % total)

########
# PART 2
########

allergenIngredients = identityAllergens(ingredientPossibleAllergens)

print('Ingredients with allergens:')
print('---------------------------')
print('\n'.join(['%-10s --> %s' % (ingredient, allergen) for allergen, ingredient in allergenIngredients.items()]))
print('---------------------------')
print('2) Canonical dangerous ingredient list: "%s"\n' % ','.join(allergenIngredients.values()))