import json

PAULA_WEIGHT = 0.1
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
        
# Calculate score for each product
for brand in product_ingredient_map:
    for product in product_ingredient_map[brand]:
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
        if (number_scores == 0):
            # ewg did not score this product
            final_scores[product] = 0
        else:
            # Scores were out of 10, 10 being worst. 
            final_scores[product] = 10 - (total_score / (number_scores))
        # Apply bonus weight for appearing in categories on paulaschoice.com
        final_scores[product] += (PAULA_WEIGHT * health_count) 
    
write_json(final_scores)
    