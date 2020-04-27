from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from flask import request
# from findation import FindationBrowser
# import time

project_name = "Save Face"
net_id = "ja523, me363, mii7, npk29"

@irsystem.route("/", methods=["GET"])
def search():
    # query = request.args.get("search")
    # if not query:
    #     data = []
    #     output_message = "Its not working"
    # else:
    #     data = range(5)
    #     output_message = "Your search: " + query
    # # query = query.split()
    # # brand1 = "Mary Kay"
    # # product1 = "Full-Coverage Foundation"
    # # shade1 = "Bronze 507"

    # # brand2 = "Mary Kay"
    # # product2 = "Medium-Coverage Foundation "
    # # shade2 = "Bronze 507 (Natural)"

    # # products = [[brand1, product1, shade1], [brand2, product2, shade2]]
    # # f = FindationBrowser()
    # # f.start()
    # # time.sleep(1)
    # # data = f.process_matches(products)
    # # f.close_out()
    # return render_template("search.html", name=project_name, netid=net_id, output_message=output_message, data=data)
    query = request.args.get("search")
    if not query:
        data = []
        output_message = "Its not working"
    else:
        data = range(5)
        output_message = "Your search: " + query
    return render_template("search.html", name=project_name, netid=net_id, output_message=output_message, data=data)
    # return (request.form['search'])

@irsystem.route("/product", methods=["GET"])
def product():
    # prod_type = request.form['choices-single-defaul']
    query = request.args.get("search")
    if not query:
        data = []
        output_message = "Its not working"
    else:
        data = range(5)
        output_message = "Your search: " + query
    return render_template("product.html", name=project_name, netid=net_id, output_message=output_message, data=data)
    # return (request.form['search'])


@irsystem.route("/outputs", methods=["POST"])
def outputs():
    # prod_type = request.form['choices-single-defaul']
    query = request.args.get("search")
    if not query:
        data = []
        output_message = "Its not working"
    else:
        data = range(5)
        output_message = "Your search: " + query
    return render_template("outputs.html", name=project_name, netid=net_id, output_message=output_message, data=data)