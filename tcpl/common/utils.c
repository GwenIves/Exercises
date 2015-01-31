#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include "utils.h"

void x_gettimeofday (struct timeval * tv) {
	if (gettimeofday (tv, NULL) == -1) {
		fprintf (stderr, "Unable to retrieve local time\n");
		exit (EXIT_FAILURE);
	}
}

struct timeval time_diff (struct timeval * before, struct timeval * after) {
	struct timeval diff;

	diff.tv_sec = after->tv_sec - before->tv_sec;
	diff.tv_usec = after->tv_usec - before->tv_usec;

	if (diff.tv_usec < 0) {
		diff.tv_usec += 1000000;
		diff.tv_sec--;
	}

	return diff;
}

ssize_t x_getline (char ** line, FILE * file) {
	size_t allocated = 0;

	ssize_t len = getline (line, &allocated, file);

	if (len == -1) {
		free (*line);
		return -1;
	} else if ((*line)[len - 1] == '\n') {
		(*line)[--len] = '\0';
	}

	return len;
}

void * x_malloc (size_t size) {
	void * mem = malloc (size);

	if (!mem) {
		fprintf (stderr, "Unable to allocate memory\n");
		exit (EXIT_FAILURE);
	}

	return mem;
}

void * x_realloc (void * ptr, size_t size) {
	void * mem = realloc (ptr, size);

	if (size > 0 && !mem) {
		fprintf (stderr, "Unable to allocate memory\n");
		exit (EXIT_FAILURE);
	}

	return mem;
}

/*
 * Prints a histogram of size non-negative values
 * If scale > 0, all values are proportionately scaled so that max == scale
 * draws either vertically or horizontally based on the vertical flag value
 */
void print_histogram (const int * values_in, size_t size, bool vertical, int scale) {
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

		for (int i = 0; i < max_value; i++)
			putchar ('-');

		putchar ('\n');
	}
}

int int_cmp (const void * a, const void * b) {
	int aa = * ((int *) a);
	int bb = * ((int *) b);

	return aa - bb;
}

int string_cmp (const void * a, const void * b) {
	return strcmp (* (char **) a, * (char **) b);
}

int string_case_cmp (const void * a, const void * b) {
	return strcasecmp (* (char **) a, * (char **) b);
}
