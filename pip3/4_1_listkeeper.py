#!/bin/env python3

import os

def main ():
	lists = get_lists ()
	print_list (lists, "Listkeeper")

	f = get_int ("Choose filename [0 for a new file]: ", 0, len (lists))

	if f == 0:
		filename = get_new_file (".lst")
	else:
		filename = lists[f - 1]

	process_file (filename)

def get_new_file (extension):
	while True:
		filename = input ("Enter a new filename: ")

		if not filename.endswith (extension):
			filename += extension

		if os.path.exists (filename):
			print ("Filename already exists")
		else:
			return filename

def get_int (msg, minimum = None, maximum = None):
	while True:
		try:
			val = int (input (msg))

			if minimum is not None and val < minimum:
				continue
			elif maximum is not None and val > maximum:
				continue
			else:
				return val
		except ValueError as err:
			print (err)

def get_lists ():
	lists = []

	for f in os.listdir ("."):
		if os.path.isfile (f) and f.endswith (".lst"):
			lists.append (f)

	return lists

def get_command (modified, empty):
	prompt = "[A]dd"
	valid = "aAqQ"

	if not empty:
		prompt += " [D]elete"
		valid += "dD"

	if modified:
		prompt += " [S]ave]"
		valid += "sS"

	prompt += " [Q]uit [a]: "

	return get_choice (prompt, valid, "a")

def get_choice (prompt, valid, default):
	while True:
		command = input (prompt)

		if not command:
			return default
		elif len (command) > 1 or command not in valid:
			print ("ERROR: invalid choice --- enter one of '{}'".format (valid))
		else:
			return command.lower ()

def print_list (list, heading):
	print ("\n{}\n".format (heading))

	size = len (list)

	if size < 10:
		width = 1
	elif size < 100:
		width = 2
	else:
		width = 3

	for num, item in enumerate (list, 1):
		print ("{0:>{2}} {1}".format (num, item, width))

	print ()

def get_items (filename):
	items = []

	try:
		with open (filename) as f:
			for item in f:
				items.append (item[:-1])
	except IOError as err:
		print (err)

	return items

def add_item (items, modified):
	item = input ("Add item: ")

	if item:
		item_lower = item.lower ()

		for i in range (len (items)):
			item_cmp = items[i].lower ()

			if item_lower < item_cmp:
				items.insert (i, item)
				return True

		items.append (item)
		return True
	else:
		return modified

def del_item (items):
	item = get_int ("Remove item: ", 1, len (items))
	del items [item - 1]

def save_items (items, filename):
	try:
		with open (filename, "w") as f:
			for item in items:
				f.write (item)
				f.write ("\n")

			print ("Writen {} lines to {}".format (len (items), filename))
	except IOError as err:
		print (err)

def process_file (filename):
	if os.path.exists (filename):
		modified = False
		lines = get_items (filename)
	else:
		modified = True
		lines = []

	lines.sort ()

	while True:
		print_list (lines, filename)

		command = get_command (modified, len (lines) == 0)

		if command == "a":
			modified = add_item (lines, modified)
		elif command == "d":
			del_item (lines)
			modified = True
		elif command == "s":
			save_items (lines, filename)
			modified = False
		else:
			if modified == True:
				prompt = "Save unsaved changes (y/n) [y]: "

				if get_choice (prompt, "yYnY", "y") == "y":
					save_items (lines, filename)

			break

main ()
