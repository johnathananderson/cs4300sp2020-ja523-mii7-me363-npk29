import json


def merge():
    with open("ingredients.json", encoding="utf8") as data:
        try:
            i = json.load(data)
            print("Opened ingredients")
        except:
            print("Couldn't open ingredients")

    with open("prices.json", encoding="utf8") as data:
        try:
            p = json.load(data)
            print("Opened prices")
        except:
            print("Couldn't open prices")

    with open("healthscores.json", encoding="utf8") as data:
        try:
            h = json.load(data)
            print("Opened scores")
        except:
            print("Couldn't open scores")

    with open("review_results-2.json", encoding="utf8") as data:
        try:
            r = json.load(data)
            print("Opened scores")
        except:
            print("Couldn't open scores")

    with open("review_words.json", encoding="utf8") as data:
        try:
            w = json.load(data)
            print("Opened scores")
        except:
            print("Couldn't open scores")

    o = {}
    for brand in i:
        o[brand] = {}
        for product_name in i[brand]:
            o[brand][product_name] = {}
            o[brand][product_name]["ingredients"] = i[brand][product_name]
            if brand in p and product_name in p[brand]:
                o[brand][product_name]["prices"] = p[brand][product_name]
            else:
                o[brand][product_name]["prices"] = []
            if brand in r and product_name in r[brand]:
                o[brand][product_name]["sentiment"] = r[brand][product_name]
            else:
                o[brand][product_name]["sentiment"] = "N/A"
            if brand in w and product_name in w[brand]:
                o[brand][product_name]["words"] = w[brand][product_name]
            else:
                o[brand][product_name]["words"] = "N/A"
            o[brand][product_name]["health_score"] = h[brand][product_name]
    with open("outputs_i1.json", "w") as outfile:
        json.dump(o, outfile, indent=4)


merge()
