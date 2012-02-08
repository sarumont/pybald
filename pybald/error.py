import exceptions

class InvalidInput(Exception):
	"""
	Exception for invalid input
	"""

	def __init__(self, msg):
		self.msg = msg
		return

	def __str__(self):
		print "Invalid input: "+self.msg

class ResourceUnavailable(Exception):
	"""Exception representing a failed request to a resource"""

	def __init__(self, msg):
		Exception.__init__(self)
		self.msg = msg

	def __str__(self):
		print "Resource unavailable: %s" % (self.msg, )
		
		
