#include <stdio.h>
#include "utils.h"

/*
 * Prints a histogram of size non-negative values
 * If scale > 0, all values are proportionately scaled so that max == scale
 * draws either vertically or horizontally based on the vertical flag value
 */
void print_histogram (int * values_in, size_t size, bool vertical, int scale) {
	int max_value = values_in[0];

	for (size_t i = 1; i < size; i++)
		if (values_in[i] > max_value)
			max_value = values_in[i];

	double scaling_factor = 1.0;

	if (scale > 0) {
		scaling_factor = scale / (double) max_value;
		max_value *= scaling_factor;
	}

	int values[size];

	for (size_t i = 0; i < size; i++)
		values[i] = values_in[i] * scaling_factor;

	if (vertical) {
		for (int i = max_value; i > 0; i--) {
			printf (" | ");

			for (size_t j = 0; j < size; j++) {
				if (values[j] >= i)
					putchar ('*');
				else
					putchar (' ');
			}

			putchar ('\n');
		}

		printf ("   ");

		for (size_t i = 0; i < size; i++)
			putchar ('-');

		putchar ('\n');
	} else {
		for (size_t i = 0; i < size; i++) {
			printf (" | ");

			for (int j = 0; j < values[i]; j++)
				putchar ('*');

			putchar ('\n');
		}

		printf ("   ");

		for (size_t i = 0; i < max_value; i++)
			putchar ('-');

		putchar ('\n');
	}
}
