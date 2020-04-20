from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Save Face"
net_id = "ja523, me363, mii7, npk29"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query or len(query)==0:
		data = []
		output_message = "Its not working"
	else:
		output_message = "Your search: " + query
		data = query
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



