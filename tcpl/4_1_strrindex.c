/*
 * strrindex () driver program
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "utils.h"

ssize_t strrindex (const char *, const char *);

int main (int argc, char ** argv) {
	if (argc != 2)
		return 1;

	char * line = NULL;

	while (x_getline (&line, stdin) != -1) {
		printf ("%ld\n", strrindex (line, argv[1]));

		free (line);
	}

	return 0;
}

ssize_t strrindex (const char * str, const char * pat) {
	if (str[0] == '\0' || pat[0] == '\0')
		return -1;

	ssize_t i = 0;

	for (i = strlen (str) - strlen (pat); i >= 0; i--) {
		size_t k = 0;

		for (size_t j = i; pat[k] != '\0'; j++, k++)
			if (str[j] != pat[k])
				break;

		if (pat[k] == '\0')
			return i;
	}

	return -1;
}
