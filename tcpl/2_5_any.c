/*
 * A driver program for any (), a strpbrk () replacement
 */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "utils.h"

static ssize_t any (const char *, const char *);

int main (int argc, char ** argv) {
	if (argc != 2)
		return 1;

	char * pattern = argv[1];

	char * line = NULL;

	while (x_getline (&line, stdin) != -1) {
		printf ("%ld\n", any (line, pattern));

		free (line);
	}

	return 0;
}

static ssize_t any (const char * str, const char * pattern) {
	ssize_t i = 0;

	for (i = 0; str[i] != '\0'; i++)
		if (strchr (pattern, str[i]))
			return i;

	return -1;
}
