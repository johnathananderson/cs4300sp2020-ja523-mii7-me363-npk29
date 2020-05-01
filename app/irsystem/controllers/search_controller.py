from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import json
import glob
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# from search import main_function
from flask import request
from findation import FindationBrowser

# import time

project_name = "Save Face"
net_id = "ja523, me363, mii7, npk29"
outputs_json = glob.glob("outputs_i.json")
with open(outputs_json[0], encoding="utf8") as data:
    try:
        outputs_j = json.load(data)
    except:
        print("Couldn't open outputs")
        outputs_j = {}


@irsystem.route("/", methods=["GET"])
def search():
    query = request.args.get("search")
    brands_json = glob.glob("brand-ids.json")
    with open(brands_json[0], encoding="utf8") as brandslist:
        bdata = json.load(brandslist)
    brands = []
    for brand in bdata:
        brands.append(brand)
    if not query:
        data = []
        output_message = "Its not working"
    else:
        output_message = "Your search: " + query
        data = range(5)
    return render_template(
        "search.html", name=project_name, netid=net_id, output_message=output_message, data=data, brands=brands
    )
    # return (request.form['search'])


@irsystem.route("/product/", methods=["GET", "POST"])
def product():
    if request.method == "GET":
        # prod_type = request.form['choices-single-defaul']
        query = request.args.get("search").strip()
        # selected_product = request.args.get("product_search") need to write form for input
        if not query:
            data = []
            output_message = "Please go back and enter a brand!"
        else:
            products_json = glob.glob("products.json")
            with open(products_json[0], encoding="utf8") as prodlist:
                pdata = json.load(prodlist)
                p = pdata[query]["products"]
            products = []
            for product in p:
                products.append(product)
            # shades = pdata[query]['products'][selected_product]['shades']

            data = range(5)
            output_message = "Your search: " + query

        return render_template(
            "product.html",
            name=project_name,
            netid=net_id,
            output_message=output_message,
            data=data,
            products=products,
            brand=query,
        )
    else:
        brand = request.form.get("brand-input")
        product = request.form.get("product-input")
        products_json = glob.glob("products.json")
        with open(products_json[0], encoding="utf8") as prodlist:
            pdata = json.load(prodlist)
            s = pdata[brand]["products"][product]["shades"]
        shades = []
        for shade in s:
            shades.append(shade)

        return render_template(
            "shades.html", name=project_name, netid=net_id, product=product, shades=shades, brand=brand
        )


@irsystem.route("/product/findation/", methods=["POST"])
def product_test():
    brand = request.form.get("brand-input")
    product = request.form.get("product-input")
    shade = request.form.get("shade-input")
    f = FindationBrowser()
    products = [[brand, product, shade], [brand, product, shade]]
    time.sleep(0.01)
    data = f.process_matches(products, outputs_j)
    f.close_out()
    return render_template("outputs.html", name=project_name, netid=net_id, data=data)


@irsystem.route("/outputs/", methods=["GET"])
def outputs():
    # prod_type = request.form['choices-single-defaul']
    query = request.args.get("adv-search")
    print(query)
    if not query:
        data = []
        output_message = "Its not working"
    else:
        data = range(5)
        output_message = "Your search: " + query
    return render_template("outputs.html", name=project_name, netid=net_id, output_message=output_message, data=data)

# @irsystem.route("/product-shades/", methods=["GET"])
# def product_shades():
#     return render_template("product-shades.html", name=project_name, netid=net_id)