import json


def merge():
    with open("ingredients.json", encoding="utf8") as data:
        try:
            i = json.load(data)
            print("Opened ingredients")
        except:
            print("Couldn't open ingredients")

    with open("prices_subset_i.json", encoding="utf8") as data:
        try:
            p = json.load(data)
            print("Opened prices")
        except:
            print("Couldn't open ingredients")

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
    with open("outputs_i.json", "w") as outfile:
        json.dump(o, outfile, indent=4)


merge()
