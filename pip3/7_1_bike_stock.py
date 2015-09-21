#!/bin/env python3

import os
import struct
import tempfile

class BinaryRecordFile:
	def __init__ (self, filename, record_size):
		self.__record_size = record_size

		if os.path.exists (filename):
			self.__fh = open (filename, "r+b")
			self.__size = self.__size ()
		else:
			self.__fh = open (filename, "w+b")
			self.__size = 0

	def close (self):
		self.__fh.close ()

	def append (self, record):
		self.__size += 1
		self[self.__size - 1] = record

	def __len__ (self):
		return self.__size

	def __setitem__ (self, index, record):
		if not isinstance (record, (bytes, bytearray)):
			raise ValueError ("Invalid type to set: " + type (record))
		elif len (record) != self.__record_size:
			raise ValueError ("Record to set must be exactly {} bytes long".format (self.__record_size))

		self.__seek_to_index (index)
		self.__fh.write (record)

	def __getitem__ (self, index):
		self.__seek_to_index (index)

		return self.__fh.read (self.__record_size)

	def __delitem__ (self, index):
		self.__seek_to_index (index)

		for i in range (index + 1, self.__size):
			self[index] = self[i]
			index += 1

		self.__size -= 1
		self.__fh.seek (self.__size * self.__record_size)
		self.__fh.truncate ()

	def __seek_to_index (self, index):
		if index >= self.__size:
			raise IndexError ("No record at index {}".format (index))

		self.__fh.seek (index * self.__record_size)

	def __size (self):
		self.__fh.seek (0, os.SEEK_END)

		return self.__fh.tell () // self.__record_size

def brf_test ():
	filename = os.path.join (tempfile.gettempdir (), "test.dat")

	if os.path.exists (filename):
		os.remove (filename)

	f = BinaryRecordFile (filename, 10)

	S = struct.Struct ("<10s")

	f.append (S.pack (b"Alpha"))
	f.append (S.pack (b"Beta"))
	f.append (S.pack (b"Gamma"))

	for i in range (len (f)):
		print (f[i])

	print ()

	del f[1]
	f.append (S.pack (b"Omega"))

	for i in range (len (f)):
		print (f[i])

	print ()

	f[1] = S.pack (b"Cyprus")

	for i in range (len (f)):
		print (f[i])

	f.close ()

def main ():
	brf_test ()

main ()
