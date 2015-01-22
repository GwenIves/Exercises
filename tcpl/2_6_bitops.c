/*
 * A driver program for bitwise operators
 */

#include <stdlib.h>
#include <stdio.h>

static unsigned long setbits (unsigned long, size_t, size_t, unsigned long);
static unsigned long invertbits (unsigned long, size_t, size_t);
static unsigned long rightrotate (unsigned long, size_t);

int main (int argc, char ** argv) {
	if (argc != 2)
		return 1;

	unsigned long num = strtoul (argv[1], NULL, 10);

	printf ("%-30s%lu\n", "setbits 3, 4, 15", setbits (num, 3, 4, 15UL));
	printf ("%-30s%lu\n", "setbits 10, 5, 1460", setbits (num, 10, 5, 1460UL));

	printf ("%-30s%lu\n", "invertbits 3, 4", invertbits (num, 3, 4));
	printf ("%-30s%lu\n", "invertbits 10, 5", invertbits (num, 10, 5));

	printf ("%-30s%lu\n", "rightrotate 3", rightrotate (num, 3));
	printf ("%-30s%lu\n", "rightrotate 10", rightrotate (num, 10));

	return 0;
}

static unsigned long setbits (unsigned long dst, size_t at, size_t size, unsigned long src) {
	unsigned long mask = ~(~0UL << size);

	src &= mask;
	src <<= at + 1 - size;

	mask = ~(mask << (at + 1 - size));
	dst &= mask;

	return dst | src;
}

static unsigned long invertbits (unsigned long bits, size_t at, size_t size) {
	unsigned long mask = ~(~0UL << size) << (at + 1 - size);

	unsigned long inverted = ~bits & mask;
	bits &= ~mask;

	return bits | inverted;
}

static unsigned long rightrotate (unsigned long bits, size_t size) {
	unsigned long right_side = bits & ~(~0UL << size);

	bits >>= size;
	right_side <<= ((sizeof (bits) << 3) - size);

	return bits | right_side;
}
