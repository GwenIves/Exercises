/*
 * atof () driver program
 */

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <math.h>
#include "utils.h"

static double x_atof (const char *);

int main (void) {
	char * line = NULL;

	while (x_getline (&line, stdin) != -1) {
		printf ("%.8g\n", x_atof (line));

		free (line);
	}

	return 0;
}

static double x_atof (const char * str) {
	while (isspace (*str))
		str++;

	int sign = 1;

	if (*str == '-') {
		sign = -1;
		str++;
	} else if (*str == '+')
		str++;

	double val = 0.0;
	int power = 0;

	while (isdigit (*str)) {
		int digit = *str - '0';
		str++;

		val *= 10;
		val += digit;
	}

	if (*str == '.')
		str++;

	while (isdigit (*str)) {
		int digit = *str - '0';
		str++;

		val *= 10;
		val += digit;
		power -= 1;
	}

	if (toupper (*str) == 'E')
		str++;

	if (isdigit (*str))
		power += atoi (str);

	return sign * val * pow (10, power);
}
