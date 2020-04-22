import json


def merge():
    with open("ingredients.json", encoding="utf8") as data:
        try:
            i1 = json.load(data)
            print("Opened ingredients")
        except:
            print("Couldn't open ingredients")

    with open("ingredients2.json", encoding="utf8") as data:
        try:
            i2 = json.load(data)
            print("Opened ingredients")
        except:
            print("Couldn't open ingredients")

    i3 = {}
    for brand in i1:
        i3[brand] = {}
        for product_name in i1[brand]:
            i3[brand][product_name] = i1[brand][product_name]

    for brand in i2:
        i3[brand] = i3.get(brand, {})
        for product_name in i2[brand]:
            i3[brand][product_name] = i3[brand].get(product_name, i2[brand][product_name])

    with open("ingredients3.json", "w") as outfile:
        json.dump(i3, outfile, indent=4)


merge()
