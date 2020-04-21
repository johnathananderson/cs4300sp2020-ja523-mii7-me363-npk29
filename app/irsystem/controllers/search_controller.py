from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from findation import *

project_name = "Save Face"
net_id = "ja523, me363, mii7, npk29"

@irsystem.route('/', methods=['GET'])
def search():
	# query = request.args.get('search')
	# if not query or len(query)==0:
	# 	data = []
	# 	output_message = "Its not working"
	# else:
	# 	output_message = "Your search: " + query   
	# 	query = query.split()
	# 	brand1 = "Mary Kay"
	# 	product1 = "Full-Coverage Foundation"
	# 	shade1 = "Bronze 507"

	# 	brand2 = "Mary Kay"
	# 	product2 = "Medium-Coverage Foundation "
	# 	shade2 = "Bronze 507 (Natural)"

	# 	products = [[brand1, product1, shade1], [brand2, product2, shade2]]
	# 	data = process_matches(products)
	
	# return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)

	pass 


