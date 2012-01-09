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

class ResourceUnavailable(Exception):
	"""Exception representing a failed request to a resource"""

	def __init__(self, msg):
		Exception.__init__(self)
		self._msg = msg

	def __str__(self):
		print "Resource unavailable: %s" % (self._msg, )
		
		
