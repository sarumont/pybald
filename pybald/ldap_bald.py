import sys
import os
import ConfigParser
import ldap

def connect(server=None, dn=None, pw=None, profile="default"):
	"""Connects to an LDAP server. Attempts to read configuration from ~/.ldap.cfg. Falls back to 
	stdin for bind credentials

	:return: an LDAP connection handle. The consumer is responsible for closing this resource when 
	done with it
	"""

	config = ConfigParser.ConfigParser()
	config.read(os.getenv('HOME')+"/.ldap.cfg")

	if not server:
		server = config.get(profile, "server")
		if not server:
			server = raw_input("LDAP server: ")

	if not dn:
		dn = config.get(profile, "binddn")
		if not dn:
			dn = raw_input("Bind DN: ")

	if not pw:
		pw = config.get(profile, "bindpw")
		if not pw:
			pw = getpass.getpass("Bind password: ");

	try:
		conn = ldap.initialize(server)
		conn.simple_bind_s(dn, pw)
	except ldap.INVALID_CREDENTIALS:
		print "Bind DN and/or Password is incorrect"
		sys.exit(1)
	except ldap.LDAPError, e:
		print "Unexpected error:", sys.exc_info()[0]
		print e
		sys.exit(1)
	return conn

if __name__ == "__main__":
	connect()
