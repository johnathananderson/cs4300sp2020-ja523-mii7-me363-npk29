import json


def merge():
    with open("outputs_i.json", encoding="utf8") as data:
        try:
            o = json.load(data)
            print("Opened outputs")
        except:
            print("Couldn't open outputs")

    with open("healthscores.json", encoding="utf8") as data:
        try:
            h = json.load(data)
            print("Opened health scores")
        except:
            print("Couldn't open health scores")

    n = {}
    for brand in o:
        n[brand] = {}
        for product_name in o[brand]:
            n[brand][product_name] = o[brand][product_name] 
            n[brand][product_name]["health_score"] = h[brand][product_name]
    with open("outputs_h.json", "w") as outfile:
        json.dump(n, outfile, indent=4)


merge()
