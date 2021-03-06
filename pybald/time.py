import re
import sys
from datetime import timedelta
from error import InvalidInput

# constants
MICROSECOND = 1
MILLISECOND = 1000
SECOND = 1000*1000
MINUTE = 1000*1000*60
HOUR = 1000*1000*60*60
DAY = 1000*1000*60*60*24
WEEK = 1000*1000*60*60*24*7

# global for the pattern
duration_regex = re.compile("((?:\d*\.\d+)|(?:\d+\.?\d*))\s*([a-zA-Z]+)")
duration_help_text = "Enter a duration of the format 1d2h3m4s"

class Duration():

	_micros = 0

	def __init__(self, value):
		if value == None:
			self._micros = 0
		elif isinstance(value, str) or isinstance(value, unicode):
			self._micros = Duration.parse(value)
		elif isinstance(value, long) or isinstance(value, int) or isinstance(value, float):
			self._micros = value
		else:
			raise InvalidInput("Cannot create Duration from "+str(type(value)))

	@staticmethod
	def parse(string):
		"""
		Parses a string representing a duration (i.e. 1h2m3s) into a Duration
		"""
		matches = duration_regex.findall(string)
		us = 0
		for m in matches:
			factor = Duration.parse_unit(m[1])
			us += float(m[0]) * factor
		return us

	@staticmethod
	def parse_unit(string):
		""" 
		Parses a string which should represent a unit of time measure, returning the factor to multiply
		a value by to convert to microseconds
		"""

		if string == "us":
			return MICROSECOND
		elif string == "ms":
			return MILLISECOND
		elif string == "s" or string == "sec" or string == "secs" or string == "seconds":
			return SECOND
		elif string == "m" or string == "min" or string == "mins" or string == "minutes":
			return MINUTE
		elif string == "h" or string == "hour" or string == "hours":
			return HOUR
		elif string == "d" or string == "day" or string == "days":
			return DAY
		elif string == "w" or string == "week" or string == "weeks":
			return WEEK
		else:
			raise InvalidInput("Cannot determine time unit from string: "+string)

	def format(self):
		""" Formats this duration as a String of the format 1d2h3m """
		micros = self.get_micros();

		if micros == 0:
			return "0"

		# start with the highest
		formatted = ""
		weeks = int(micros / WEEK)
		if weeks > 0:
			micros -= weeks*WEEK
			formatted += str(weeks) + "w"

		days = int(micros / DAY)
		if days > 0:
			micros -= days*DAY
			formatted += str(days) + "d"

		hours = int(micros / HOUR)
		if hours > 0:
			micros -= hours*HOUR
			formatted += str(hours) + "h"

		minutes = int(micros / MINUTE)
		if minutes > 0:
			micros -= minutes*MINUTE
			formatted += str(minutes) + "m"

		seconds = int(micros / SECOND)
		if seconds > 0:
			micros -= seconds*SECOND
			formatted += str(seconds) + "s"

		millis = int(micros / MILLISECOND)
		if millis > 0:
			micros -= millis*MILLISECOND
			formatted += str(millis) + "ms"

		if micros > 0:
			formatted += str(int(micros)) + "us"
		return formatted

	def get_micros(self):
		""" returns the number of microseconds in this duration """
		return self._micros

	def get_seconds(self):
		""" Returns the number of whole seconds in this duration """
		micros = self._micros
		if micros == 0:
			return 0
		weeks = int(micros / WEEK)
		if weeks > 0:
			micros -= weeks*WEEK
		days = int(micros / DAY)
		if days > 0:
			micros -= days*DAY
		hours = int(micros / HOUR)
		if hours > 0:
			micros -= hours*HOUR
		minutes = int(micros / MINUTE)
		if minutes > 0:
			micros -= minutes*MINUTE
		return int(micros / SECOND)

	def get_minutes(self):
		""" Returns the number of whole minutes in this duration """
		micros = self._micros
		if micros == 0:
			return 0
		weeks = int(micros / WEEK)
		if weeks > 0:
			micros -= weeks*WEEK
		days = int(micros / DAY)
		if days > 0:
			micros -= days*DAY
		hours = int(micros / HOUR)
		if hours > 0:
			micros -= hours*HOUR
		return int(micros / MINUTE)

	def get_hours(self):
		""" Returns the number of whole hours in this duration """
		micros = self._micros
		if micros == 0:
			return 0
		weeks = int(micros / WEEK)
		if weeks > 0:
			micros -= weeks*WEEK
		days = int(micros / DAY)
		if days > 0:
			micros -= days*DAY
		return int(micros / HOUR)

if __name__ == "__main__":
	dur = Duration(sys.argv[1])
	#print("timedelta: " + str(td))
	print("micros: " + str(dur.get_micros()))
	print("formatted: " + dur.format())
