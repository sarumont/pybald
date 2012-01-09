from pybald.error import InvalidInput,ResourceUnavailable
from httplib2 import Http
from urllib import quote
import json

def launder(num):
	"""Returns a laundered phone number using the service at http://numberlaundry.whatcheer.com/

	:num: raw phone number input
	:return: a number of the form +13030000000
	"""

	client = Http()
	headers = {'Accept': 'application/json'}
	url = 'http://numberlaundry.whatcheer.com/launder/'+quote(num)
	response, content = client.request(url, 'GET', headers = headers)

	# error checking
	if response.status != 200:
		raise ResourceUnavailable(url)

	json_obj = json.loads(content)
	if json_obj['error']:
		raise InvalidInput(num)

	return json_obj['clean']
