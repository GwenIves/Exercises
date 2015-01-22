/*
 * Filter characters specified on the command line from stdin
 */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "utils.h"

static void squeeze (char *, const char *);

int main (int argc, char ** argv) {
	if (argc != 2)
		return 1;

	char * pattern = argv[1];

	char * line = NULL;

	while (x_getline (&line, stdin) != -1) {
		squeeze (line, pattern);

		printf ("%s\n", line);

		free (line);
	}

	return 0;
}

static void squeeze (char * str, const char * pattern) {
	size_t j = 0;

	for (size_t i = 0; str[i] != '\0'; i++)
		if (!strchr (pattern, str[i]))
			str[j++] = str[i];

	str[j] = '\0';
}
