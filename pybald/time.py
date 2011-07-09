import re
import sys
from datetime import timedelta
from error import InvalidInput

# global for the pattern
duration_regex = re.compile("((?:\d*\.\d+)|(?:\d+\.?\d*))\s*([a-zA-Z]+)")

def parse_duration(string):

	matches = duration_regex.findall(string)
	us = 0
	for m in matches:
		factor = parse_unit(m[1])
		us += float(m[0]) * factor
	return timedelta(microseconds = us)

def parse_unit(string):
	""" 
	Parses a string which should represent a unit of time measure, returning the factor to multiply
	a value by to convert to microseconds
	"""

	if string == "us":
		return 1
	elif string == "ms":
		return 1000
	elif string == "s" or string == "sec" or string == "secs" or string == "seconds":
		return 1000*1000
	elif string == "m" or string == "min" or string == "mins" or string == "minutes":
		return 1000*1000*60
	elif string == "h" or string == "hour" or string == "hours":
		return 1000*1000*60*60
	elif string == "d" or string == "day" or string == "days":
		return 1000*1000*60*60*24
	elif string == "w" or string == "week" or string == "weeks":
		return 1000*1000*60*60*24*7
	else:
		raise InvalidInput("Cannot determine time unit from string: "+string)


if __name__ == "__main__":
	parse_duration(sys.argv[1])
