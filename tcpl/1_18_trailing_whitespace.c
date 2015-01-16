/*
 * Remove trailing whitespace from stdin
 */

#include <stdlib.h>
#include <ctype.h>
#include "utils.h"

int main (void) {
	char * line = NULL;
	ssize_t len = 0;

	while ((len = x_getline (&line, stdin)) != -1) {
		int i = 0;

		for (i = len - 1; i >= 0; i--)
			if (!isblank (line[i]))
				break;

		if (i >= 0) {
			line[i + 1] = '\0';
			printf ("%s\n", line);
		}

		free (line);
	}

	return 0;
}
