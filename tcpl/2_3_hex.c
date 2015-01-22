/*
 * Convert hex numbers on stdin, one per line, to decimal
 */

#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include "utils.h"

static int htoi (const char *);

int main (void) {
	char * line = NULL;

	while (x_getline (&line, stdin) != -1) {
		printf ("%d\n", htoi (line));

		free (line);
	}

	return 0;
}

static int htoi (const char * str) {
	int value = 0;
	int sign = 1;

	if (str[0] == '-') {
		sign = -1;
		str++;
	}

	if (str[0] == '0' && tolower (str[1]) == 'x')
		str += 2;

	char digit = 0;

	while ((digit = tolower (*str)) != '\0') {
		int digit_value = 0;

		if (isdigit (digit))
			digit_value = digit - '0';
		else if (digit >= 'a' && digit <= 'f')
			digit_value = digit - 'a' + 10;
		else
			break;

		value *= 16;
		value += digit_value;

		str++;
	}

	return value * sign;
}
