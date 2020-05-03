import json

PAULA_WEIGHT = 0.013
def write_json(data, filename='healthscores.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4)
        
with open("ingredients_score_map.json", encoding = 'utf-8') as j:
    ingredient_scores = json.load(j)
    
with open("ingredients.json", encoding = 'utf-8') as j:
    product_ingredient_map = json.load(j)

with open("ingredient_categories.json", encoding = 'utf-8') as j:
    data = json.load(j)
final_scores = {}
ingredient_set = set()

# Create paulaschoice.com ingredient dictionary
for cat in data:
    for ingredient in data[cat]:
        ingredient_set.add(ingredient)
        
#Normalization values
listmin = float("inf")
listmax = float("-inf")
# Calculate score for each product
for brand in product_ingredient_map:
    final_scores[brand] = {}
    for product in product_ingredient_map[brand]:
        if product_ingredient_map[brand][product] == "Ingredients not found":
            final_scores[brand][product] = "N/A"
            continue
        total_score = 0
        number_scores = 0
        health_count = 0
        for ingredient in product_ingredient_map[brand][product]:
            # If ingredient appears in ANY of paulaschoice.com categories,
            # add some weight to this product via health_count. 
            for i in ingredient_set:
                if i in ingredient.lower():
                    health_count += 1
            # Calculating average product ewg score with total_score and number_scores
            total_score += ingredient_scores[ingredient]
            if (ingredient_scores[ingredient] > 0):
                number_scores += 1
        if (total_score == 0):
            # ewg did not score this product
            if health_count > 0:
                final_scores[brand][product] = min(10, health_count + 5)
            else:
                final_scores[brand][product] = "N/A"
                continue
        else:
            # Scores were out of 10, 10 being worst. 
            final_scores[brand][product] = 10 - (total_score / (number_scores))
        # Apply bonus weight for appearing in categories on paulaschoice.com
        final_scores[brand][product] = min(final_scores[brand][product] + (PAULA_WEIGHT * health_count), 10)
        listmin = min(listmin,final_scores[brand][product])
        listmax = max(listmax, final_scores[brand][product])
# counta = 0
# countb = 0
# countc = 0
# countd = 0
# counte = 0
# countf = 0
# countg = 0
# counth = 0
# counti = 0
# countj = 0
# total = 0

for brand in final_scores:
    for product in final_scores[brand]:
        val = final_scores[brand][product]
        if (val == "N/A"):
            continue
        final_scores[brand][product] = round(((val-listmin) / (listmax-listmin)) * 10, 2)
        # if (final_scores[brand][product] >= 9):
        #     counta += 1
        # elif (final_scores[brand][product] >= 8 and final_scores[brand][product] < 9):
        #     countb += 1
        # elif (final_scores[brand][product] >= 7 and final_scores[brand][product] < 8):
        #     countc += 1
        # elif (final_scores[brand][product] >= 6 and final_scores[brand][product] < 7):
        #     countd += 1
        # elif (final_scores[brand][product] >= 5 and final_scores[brand][product] < 6):
        #     counte += 1
        # elif (final_scores[brand][product] >= 4 and final_scores[brand][product] < 5):
        #     countf += 1
        # elif (final_scores[brand][product] >= 3 and final_scores[brand][product] < 4):
        #     countg += 1
        # elif (final_scores[brand][product] >= 2 and final_scores[brand][product] < 3):
        #     counth += 1
        # elif (final_scores[brand][product] >= 1 and final_scores[brand][product] < 2):
        #     counti += 1
        # elif (final_scores[brand][product] >= 0 and final_scores[brand][product] < 1):
        #     countj += 1
        # total += 1
# print(counta/total)
# print(countb/total)
# print(countc/total)
# print(countd/total)
# print(counte/total)
# print(countf/total)
# print(countg/total)
# print(counth/total)
# print(counti/total)
# print(countj/total)
write_json(final_scores)
    