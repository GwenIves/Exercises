#!/bin/env python3

import math

class point:
	def __init__ (self, x=0, y=0):
		self.x = x
		self.y = y

	def __eq__ (self, other):
		return self.x == other.x and self.y == other.y

	def __repr__ (self):
		return "point({0.x!r}, {0.y!r})".format (self)

	def __str__ (self):
		return "({0.x!s}, {0.y!s})".format (self)

	def __add__ (self, other):
		return point (self.x + other.x, self.y + other.y)

	def __iadd__ (self, other):
		self.x += other.x
		self.y += other.y

		return self

	def __sub__ (self, other):
		return point (self.x - other.x, self.y - other.y)

	def __isub__ (self, other):
		self.x -= other.x
		self.y -= other.y

		return self

	def __mul__ (self, n):
		return point (self.x * n, self.y * n)

	def __imul__ (self, n):
		self.x *= n
		self.y *= n

		return self

	def __truediv__ (self, n):
		return point (self.x / n, self.y / n)

	def __itruediv__ (self, n):
		self.x /= n
		self.y /= n

		return self

	def __floordiv__ (self, n):
		return point (self.x // n, self.y // n)

	def __ifloordiv__ (self, n):
		self.x //= n
		self.y //= n

		return self

	def distance_from_origin (self):
		return math.hypot (self.x, self.y)

def main ():
	a = point ()
	b = point (3, 4)

	print (a)
	print ("{!r}".format (b))
	print ()

	print (a.distance_from_origin ())
	print (b.distance_from_origin ())
	print ()

	c = a + b
	print (b == c)
	print ()

	a += point (1, 1)
	print (a)
	print ()

	c -= point (1, 1)
	print (c)
	print ()

	d = b * 2
	print (d)
	print ()

	print (d / 3)
	print (d // 3)
	print ()

main ()
