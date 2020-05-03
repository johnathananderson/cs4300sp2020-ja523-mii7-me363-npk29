import json
import requests

with open("./brand-ids.json") as j:
    data = json.load(j)

base_url = "https://findation.com/"
brand_prefix = "products?brand_id="
brand_suffix = "&include_discontinued=true&src=findation"
product_prefix = "shades?product_id="

new_data = {}

for brand in data:
    print(brand)
    brand_url = base_url + brand_prefix + str(data[brand]["id"]) + brand_suffix
    response = json.loads(requests.get(brand_url).content.decode("utf-8"))
    if len(response) > 0:
        new_data[brand.strip()] = data[brand]
        new_data[brand.strip()]["products"] = {}
        for product in response:
            p = {}
            product_name = product["name"]
            p["id"] = product["id"]
            p["thumb_image_url"] = product["thumb_image_url"]
            p["micro_image_url"] = product["micro_image_url"]
            p["shades"] = {}
            product_url = base_url + product_prefix + str(product["id"])
            shades = json.loads(requests.get(product_url).content.decode("utf-8"))
            for shade in shades:
                s = {}
                shade_name = shade["name"]
                s["id"] = shade["id"]
                p["shades"][shade_name] = s
            new_data[brand.strip()]["products"][product_name.strip()] = p
        with open("products_1.json", "w") as outfile:
            json.dump(new_data, outfile, indent=4)
