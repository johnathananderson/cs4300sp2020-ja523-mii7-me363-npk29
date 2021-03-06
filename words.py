# -*- coding: utf-8 -*-
"""Untitled.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AXgvUCZrPW4RsStFG27aaQ_8jXrII_G1
"""

import json
from nltk.corpus import stopwords
import nltk
import pandas as pd
import numpy as np
from nltk.tokenize import RegexpTokenizer

ulta = pd.read_csv("/content/ulta.csv")
beautypedia = pd.read_csv("/content/merged.csv")

print(ulta)

print(ulta["brand"])

print(ulta["name"])
name = ulta["name"]

print(ulta["reviews-text"])

ulta_reviews = (ulta["reviews-text"].dropna())
print(ulta_reviews)

print(ulta.name[ulta_reviews])

ultadf = pd.DataFrame(ulta, columns=['brand', 'name', 'reviews-text'])

ultadf.head()

ultadf = ultadf.dropna().reset_index(drop=True)

ultadf.head()

pd.set_option('display.max_rows', None)
print(ultadf)

ultadf.iloc[124]["reviews-text"]

# beautypediadf = pd.DataFrame(ulta, columns = ['brand','name', 'reviews-text'])
beautypedia.head()
beautypediadf = pd.DataFrame(
    beautypedia, columns=['brand', 'name', 'community-review-text'])
beautypediadf = beautypediadf.dropna().reset_index(drop=True)

beautypediadf.head()

beautypediadf.iloc[4267]["community-review-text"]

ultadf.head()
beautypediadf.head()

print(len(ultadf["reviews-text"]))

# Notes for Nakia
# Organized Dataframes variables below
# ultadf
# beautypediadf

# Goal: to create function that takes in a list of reviews and out puts top 3 most frequent

# first we need to loop through dataframes and for each product that has the same name, store it's reviews in a list

review_dict = {}
for index, row in ultadf.iterrows():
    review_dict[row['brand']] = {}

for index, row in beautypediadf.iterrows():
    review_dict[row['brand']] = {}


for index, row in beautypediadf.iterrows():
    review_dict[row['brand']][row['name']] = []

for index, row in ultadf.iterrows():
    review_dict[row['brand']][row['name']] = []

for index, row in beautypediadf.iterrows():
    review_dict[row['brand']][row['name']].append(row['community-review-text'])

for index, row in ultadf.iterrows():
    review_dict[row['brand']][row['name']].append(row['reviews-text'])


print(review_dict['MAC'])

nltk.download('stopwords')


stop_words = set(stopwords.words('english'))

tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')

makeup_words = ultadf["brand"].unique()
list2 = beautypediadf['brand'].unique()
makeup_words = np.append(makeup_words, list2)
# add stop words
makeup_words = np.append(makeup_words, ["foundation", "concealer", "skin", "powder", "it", "", "product", "look", "make", "use", "really", "face", "stick", "makeup", "feel", "one", "bit", "!", ".", "go", "looked", "please", "&", "wear", "wears", "bought", "<", "-", "tried", "lines",
                                        "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "ordered", "looks", "look", "looking", "would", "see", "new", "way", "every", "using", "ever", "review", "even", "always", "used", "put", "get", "cannot", "also", "wears", "end", "little", "thing", "goes", "eye", "eyes"])

makeup_words = [x.lower() for x in makeup_words]

# get number of distinct words
distinct_list = []
for keys in review_dict.keys():
    for items in review_dict[keys].keys():
        for item in review_dict[keys][items]:
            words = tokenizer.tokenize(item)
            for it in words:
                it = it.lower()
                it = it.replace('.', '')
                it = it.replace("\\", "")
                it = it.replace("/", "")
                if it not in distinct_list and it not in stop_words and it not in makeup_words:
                    distinct_list.append(it)

y = len(distinct_list)
names = ultadf["name"].unique()
names = np.append(names, beautypediadf['name'])
x = len(names)

# have to create a list of "good" words (appear more than 3 times and arent too common)

word_index = {}
reverse_w_index = {}
reverse_p_index = {}
product_index = {}
counter = 0
for word in distinct_list:
    word_index[word] = counter
    reverse_w_index[counter] = word
    counter += 1

counter2 = 0
for product in names:
    product_index[product] = counter2
    reverse_p_index[counter2] = product
    counter2 += 1


matrix = np.empty([x, y])
product_dict = {}
for words in ultadf["name"].unique():
    product_dict[words] = {}

word_dict = {}

for brand in review_dict.keys():
    for product in review_dict[brand].keys():
        for item in review_dict[brand][product]:
            words = item.split(" ")
            for word in words:
                if word in distinct_list:
                    if word not in word_dict.keys():
                        word_dict[word] = 0
                    else:
                        word_dict[word] += 1

        product_dict[product] = word_dict
        word_dict = {}

print(product_dict['Acne Solutions Liquid Makeup'])

# Add frequency scores to matrix
for product in product_dict.keys():
    for word in product_dict[product].keys():
        count = product_dict[product][word]

        index1 = product_index[product]
        index2 = word_index[word]
        matrix[index1][index2] = count


matrix[product_index['Acne Solutions Liquid Makeup']]

# Find words with most frequency


results_dict = {}
temp_dict = {}
for row in range(len(matrix)):
    top = matrix[row].argsort()[-3:][::-1]
    product = reverse_p_index[row]
    temp_dict[product] = top
    results_dict[product] = []

for products in temp_dict.keys():
    for indices in temp_dict[products]:
        word = reverse_w_index[indices]
        results_dict[products].append(word)

print(results_dict)


with open('words.json', 'w') as json_file:
    json.dump(results_dict, json_file)
