/*
 * Print stdin reversed line by line
 */

#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include "utils.h"

static void swap (char *, size_t, size_t);
static void reverse (char *, size_t len);
static void reverse_rec (char *, int, int);

int main (int argc, char ** argv) {
	char * line = NULL;
	ssize_t len = 0;

	bool recursive = false;

	int arg = 0;

	while ((arg = getopt (argc, argv, "r")) != -1) {
		switch (arg) {
			case 'r':
				recursive = true;
				break;
			case '?':
			default:
				break;
		}
	}

	while ((len = x_getline (&line, stdin)) != -1) {
		if (recursive)
			reverse_rec (line, 0, len - 1);
		else
			reverse (line, len);

		printf ("%s\n", line);

		free (line);
	}

	return 0;
}

static void reverse (char * line, size_t len) {
	if (len == 0)
		return;

	size_t start = 0;
	size_t end = len - 1;

	while (start < end) {
		swap (line, start, end);

		start++;
		end--;
	}
}

static void reverse_rec (char * line, int from, int to) {
	if (from < to) {
		swap (line, from, to);
		reverse_rec (line, from + 1, to - 1);
	}
}

static void swap (char * str, size_t i, size_t j) {
	char temp = str[i];

	str[i] = str[j];
	str[j] = temp;
}
