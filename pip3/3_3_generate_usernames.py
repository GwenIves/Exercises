#!/bin/env python3

import collections
import sys

ID, FORENAME, MIDDLENAME, SURNAME, DEPARTMENT = range (5)

NAME_WIDTH = 18
USERNAME_WIDTH = 9

User = collections.namedtuple ("User", "username forename middlename surname id")

def main ():
	users = []
	usernames = collections.defaultdict (int)

	for filename in sys.argv[1:]:
		for line in open (filename):
			line.rstrip ()

			if not line:
				continue

			user = process_line (line, usernames)
			users.append (user)

	print_users (users)

def process_line (line, usernames):
	fields = line.split (":")
	username = generate_username (fields, usernames)

	return User (username, fields[FORENAME], fields[MIDDLENAME], fields[SURNAME], fields[ID])

def generate_username (fields, usernames):
	mappings = {ord ("-") : None, ord ("'") : None}

	surname = fields[SURNAME].translate (mappings)
	username = fields[FORENAME][0] + fields[MIDDLENAME][:1] + surname;
	username = username[:8].lower ()

	usernames[username] += 1

	return username + str (usernames[username])

def print_users (users):
	users.sort (key=lambda user: ((user.surname.lower (), user.forename.lower (), user.id)))
	lineno = 0

	while True:
		user_a = None
		user_b = None

		try:
			user_a = users.pop (0)
			user_b = users.pop (0)
		except IndexError:
			pass

		if not user_a:
			break

		if lineno % 64 == 0:
			print_heading (lineno > 0)

		lineno += 1

		print_line (user_a, user_b)

def print_heading (should_break):
	if should_break:
		print ()

	print ("{0:<{nw}} {1:^6} {2:{uw}} {0:<{nw}} {1:^6} {2:{uw}} ".format (
		"Name", "ID", "Username", nw = NAME_WIDTH, uw = USERNAME_WIDTH))
	print ("{0:-<{nw}} {0:-<6} {0:-<{uw}} {0:-<{nw}} {0:-<6} {0:-<{uw}}".format (
		"", nw = NAME_WIDTH, uw = USERNAME_WIDTH))

def print_line (user_a, user_b):
	print ("{} {}".format (get_user_line (user_a), get_user_line (user_b)))

def get_user_line (user):
	if not user:
		return ""

	name = "{0.surname}, {0.forename}{1}".format (
		user, " " + user.middlename[0] if user.middlename else "")

	return "{0:.<{nw}.{nw}} ({1.id:4}) {1.username:{uw}}".format (
		name, user, nw = NAME_WIDTH, uw = USERNAME_WIDTH)

main ()
