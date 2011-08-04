import exceptions

class InvalidInput(Exception):
	"""
	Exception for invalid input
	"""

	def __init__(self, msg):
		self._msg = msg
		return

	def __str__(self):
		print "Invalid input: "+self._msg
