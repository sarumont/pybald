import re
import sys
from error import InvalidInput

# constants
GRAM_OUNCE_CONVERSION = 28.3495231

# global for the pattern
weight_regex = re.compile("((?:\d*\.\d+)|(?:\d+\.?\d*))\s*([a-zA-Z.]*)")

class Weight():
	""" Class representing the weight of an object with a base unit of grams """

	_grams = 0
	_ounces = 0
	_pounds = 0
	_imperial = True

	def __init__(self, value):
		if not value:
			pass
		elif isinstance(value, str) or isinstance(value, unicode):
			self.parse(value)
		elif isinstance(value, tuple):
			# should be pounds and ounces
			if len(value) == 2:
				self._pounds = value[0]
				self._ounces = value[1]
				self._imperial = True
			else:
				raise InvalidInput("Cannot create Weight from tuple with "+str(len(value))+" elements")
		elif isinstance(value, long) or isinstance(value, int) or isinstance(value, float):
			self._imperial = False
			self._grams = float(value)
		else:
			raise InvalidInput("Cannot create Weight from "+str(type(value)))

	def parse(self, string):
		"""
		Parses a string representing a weight (i.e. 4lbs. 3oz, 4kg) into a Weight
		"""
		matches = weight_regex.findall(string)
		for m in matches:
			num = float(m[0])
			string = m[1].strip('.')
			if string is None or string == "":
				# assume a numeric string is an imperial unit
				self._imperial = True
				self._pounds += num
			elif string == "g" or string == "gram" or string == "grams":
				self._imperial = False
				self._grams += num
			elif string == "kg" or string == "kilos" or string == "kilogram" or string == "kilograms":
				self._imperial = False
				self._grams += 1000*num
			elif string == "lb" or string == "lbs" or string == "pound" or string == "pounds":
				self._imperial = True
				self._pounds += num
			elif string == "oz" or string == "ounce" or string == "ounces":
				self._imperial = True
				self._ounces += num
			else:
				raise InvalidInput("Cannot determine weight unit from string: '"+string+"'")

		# correct for decimals
		if int(self._pounds) != self._pounds:
			delta = self._pounds - int(self._pounds)
			self._ounces += round(16*delta)

		# ensure we didn't overflow
		if self._imperial and self._ounces >= 16:
			pounds = int(self._ounces/16)
			self._ounces -= pounds*16
			self._pounds += pounds
		

	def isImperial(self):
		return self._imperial

	def format(self):
		""" 
		Formats this weight as a string
		
		Imperial: 5lbs. 3oz
		Metric: 1.35kg
		"""

		if self._imperial:
			if self._pounds > 0:
				if self._ounces > 0:
					return '%dlbs %doz' % ( self._pounds, self._ounces, )
				return '%dlbs' % ( self._pounds, )
			elif self._ounces > 0:
				return '%doz' % ( self._ounces, )
			return ''

		else:
			if self._grams >= 1000:
				return '%.3fkg' % ( self._grams/1000, )
			else:
				return '%dg' % ( self._grams, )

	def asOunces(self):
		""" 
		Returns the value of this Weight in ounces. If this object was not created with imperial
		measurements, an estimate is returned
		"""
		global GRAM_OUNCE_CONVERSION
		if self._imperial:
			return 16*self._pounds + self._ounces
		else:
			return self._grams/GRAM_OUNCE_CONVERSION

	def asGrams(self):
		""" 
		Returns the value of this Weight in grams. If this object was created with imperial
		measurements, an estimate is returned
		"""
		global GRAM_OUNCE_CONVERSION
		if self._imperial:
			return GRAM_OUNCE_CONVERSION * (16*self._pounds + self._ounces)
		else:
			return self._grams

	@staticmethod
	def decode(value):
		""" Method to decode a string generated from Weight.encode """
		if value == None:
			return Weight()
		elif value.startswith('i'):
			return Weight((0, int(value[1:None])))
		elif value.startswith('m'):
			return Weight(int(value[1:None]))
		else:
			raise InvalidInput("Cannot decode "+value+" to a Weight")

	def encode(self):
		if self._imperial:
			return "i%d" % (self.asOunces(), )
		else:
			return "m%d" % (self.asGrams(), )

if __name__ == "__main__":
	w = Weight(sys.argv[1])
	print("formatted: " + w.format() + ", grams = " + str(w.asGrams()) + ", ounces = " +
			str(w.asOunces()) + ", encoded = " + w.encode())
	w = Weight.decode(w.encode())
	#w = Weight(( 3, 13, ))
	print("formatted: " + w.format() + ", grams = " + str(w.asGrams()) + ", ounces = " +
			str(w.asOunces()) + ", encoded = " + w.encode())
