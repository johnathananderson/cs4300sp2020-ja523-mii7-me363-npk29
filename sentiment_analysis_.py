#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3

from textblob import TextBlob
import pandas as pd
import math
import json
reviews_table = pd.read_csv("ulta.csv")
reviews_table2 = pd.read_csv("merged.csv")


def get_score(reviews_dict):
    results_dict = {}
    product_score = 0

    for keys in reviews_dict.keys():
        if len(reviews_dict[keys]) == 0:
            avg_score = 0
        else:
            for review in reviews_dict[keys]:
                if type(review) == str:
                    text = TextBlob(review)
                    score = text.sentiment.polarity
                    product_score += score
            avg_score = float(product_score / len(reviews_dict[keys]))

        results_dict[keys] = avg_score
        product_score = 0

    return(results_dict)


def get_reviews(brand, products):
    reviews_dict = {}
    print("Brand: ", brand)
    for product in products:
        print(product)

        reviews1 = ""
        reviews2 = ""
        reviews3 = ""

        if any(reviews_table.name == product):
            print("Found product in Ulta!")
            brandlist = reviews_table['brand'].tolist()

            if brand in brandlist:
                print("Found Brand in Ulta!")
                brand_table = reviews_table.loc[reviews_table['brand'] == brand]
                product_rows = brand_table.loc[brand_table['name'] == product]
                reviews1 = product_rows['reviews-text'].tolist()
                reviews2 = product_rows['top-positive-review'].tolist()
                reviews3 = product_rows['top-negative-review'].tolist()
                reviews4 = product_rows['review-keyword'].tolist()
                total_review = reviews1 + reviews2 + reviews3 + reviews4

        if any(reviews_table2.name == product):
            print("Found product in Makeup!")
            brandlist2 = reviews_table2['brand'].tolist()
            if brand in brandlist2:
                print("Found Brand in Makeup!")
                product_rows2 = reviews_table2.loc[reviews_table2['name'] == product]
                reviews1 = product_rows2['review-text'].tolist()
                reviews2 = product_rows2['community-review-text'].tolist()
                reviews3 = product_rows2['keyword'].tolist()
                total_reviews2 = reviews1 + reviews2 + reviews3

        all_reviews = reviews1 + reviews2 + reviews3
        reviews_dict[product] = all_reviews
    return reviews_dict


def insertion_cost(message, j):
    return 1


def deletion_cost(query, i):
    return 1


def substitution_cost(query, message, i, j):
    if query[i-1] == message[j-1]:
        return 0
    else:
        return 1


curr_insertion_function = insertion_cost
curr_deletion_function = deletion_cost
curr_substitution_function = substitution_cost


def edit_matrix(query, message):

    m = len(query) + 1
    n = len(message) + 1

    chart = {(0, 0): 0}
    for i in range(1, m):
        chart[i, 0] = chart[i-1, 0] + curr_deletion_function(query, i)
    for j in range(1, n):
        chart[0, j] = chart[0, j-1] + curr_insertion_function(message, j)
    for i in range(1, m):
        for j in range(1, n):
            chart[i, j] = min(
                chart[i-1, j] + curr_deletion_function(query, i),
                chart[i, j-1] + curr_insertion_function(message, j),
                chart[i-1, j-1] +
                curr_substitution_function(query, message, i, j)
            )
    return chart


def edit_distance(query, message):

    query = query.lower()
    message = message.lower()
    value = edit_matrix(query, message)
    score = 0
    for keys in value.keys():
        if keys == (len(query), len(message)):
            score = value[keys]

    return(score)


def edit_distance_search(query, msgs):
    result = []
    for items in msgs:
        sentence = items
        score = edit_distance(query, sentence)
        result.append((score, items))
    result.sort(key=lambda x: x[0])

    return(result[0])


def get_product_list(product_list):
    table1 = reviews_table['name'].tolist()
    table2 = reviews_table2['name'].tolist()
    new_product_list = []
    all_table = table1 + table2
    print("Getting product list...")
    for item in product_list:
        print(item)
        if item not in table1 and item not in table2:
            print("No Reviews :(")
            score = edit_distance_search(item, all_table)
            product_name = score[1]
        else:
            print("Found Reviews :)")
            product_name = item
        new_product_list.append(product_name)

    return new_product_list


def main(brand, product_list):
    print("Getting correct product list...")
    correct_product_list = get_product_list(product_list)
    print("Found correct product list!")
    print("Getting Reviews...")
    products = get_reviews(brand, correct_product_list)
    print("Got Reviews!")
    print("Scoring Reviews...")
    results = get_score(products)
    print("Reviews scored!")

    with open('review_results.json', 'a') as fp:
        json.dump({brand: results}, fp)


f = open('product_list.json')
data = json.load(f)
f.close()

for k in data.keys():
    main(k, data[k])

# Input is a list of products
