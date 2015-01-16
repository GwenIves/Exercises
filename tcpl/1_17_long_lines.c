/*
 * Print only long lines from stdin
 */

#include <stdlib.h>
#include "utils.h"

#define MIN_LENGTH	40

int main (void) {
	char * line = NULL;
	ssize_t len = 0;

	while ((len = x_getline (&line, stdin)) != -1) {
		if (len >= MIN_LENGTH)
			printf ("%s\n", line);

		free (line);
	}

	return 0;
}
