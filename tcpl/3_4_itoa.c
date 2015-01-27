/*
 * itoa () driver program
 */

#include <stdio.h>

static void itoa (int, char *, int, int);

#define MAX_BASE	('Z' - 'A' + 1 + 10)
#define MIN_SIZE	20

int main (void) {
	int num = 0;
	int base = 0;
	int width = 0;

	while (scanf ("%d %d %d", &num, &base, &width) == 3) {
		int len = width > MIN_SIZE ? width : MIN_SIZE;

		char str[len + 1];

		itoa (num, str, base, width);

		printf ("Converted: %s\n", str);
	}

	return 0;
}

/*
 * atoi () inverse.
 * Convert an integer 'number' into a string 'str', in base 'base' (2 - 36)
 * If 'width' is given (positive), 'str' is left-padded in a field of at least the given size
 * The caller must guarantee 'str' is large enough
 */
static void itoa (int number, char * str, int base, int width) {
	if (base < 2 || base > MAX_BASE) {
		str[0] = '\0';
		return;
	}

	int num = number;

	int i = 0;

	do {
		int digit = num % base;
		num /= base;

		if (digit < 0)
			digit = -digit;

		if (digit < 10)
			str[i++] = '0' + digit;
		else
			str[i++] = 'A' + digit - 10;
	} while (num != 0);

	if (number < 0)
		str[i++] = '-';

	while (i < width)
		str[i++] = ' ';

	str[i--] = '\0';

	for (int j = 0; j < i; j++, i--) {
		char t = str[j];
		str[j] = str[i];
		str[i] = t;
	}
}
