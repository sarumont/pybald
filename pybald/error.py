import exceptions

class InvalidInput(Exception):
	"""
	Exception for invalid input
	"""

	def __init__(self, msg):
		_msg = msg
		return

	def __str__(self):
		print "Invalid input: "+_msg
