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

def format(duration):
	micros = 0
	if isinstance(duration, timedelta):
		micros = duration.microseconds + duration.seconds*1000*1000 + duration.days*1000*1000*60*60*24
	else:
		micros = duration

	# start with the highest
	formatted = ""
	weeks = micros / WEEK
	if weeks > 0:
		micros -= weeks*WEEK
		formatted += str(weeks) + "w"

	days = micros / DAY
	if days > 0:
		micros -= days*DAY
		formatted += str(days) + "d"

	hours = micros / HOUR
	if hours > 0:
		micros -= hours*HOUR
		formatted += str(hours) + "h"

	minutes = micros / MINUTE
	if minutes > 0:
		micros -= minutes*MINUTE
		formatted += str(minutes) + "m"

	seconds = micros / SECOND
	if seconds > 0:
		micros -= seconds*SECOND
		formatted += str(seconds) + "s"

	millis = micros / MILLISECOND
	if millis > 0:
		micros -= millis*MILLISECOND
		formatted += str(millis) + "ms"

	if micros > 0:
		formatted += str(micros) + "us"
	return formatted

if __name__ == "__main__":
	td = parse_duration(sys.argv[1])
	print("timedelta: " + str(td))
	print("formatted: " + format(td))
