/*
 * Print the longest line on stdin and its length
 */

#include <stdlib.h>
#include "utils.h"

int main (void) {
	char * line = NULL;
	ssize_t len = 0;

	char * longest_line = NULL;
	ssize_t max_len = 0;

	while ((len = x_getline (&line, stdin)) != -1) {
		if (len > max_len) {
			max_len = len;

			free (longest_line);
			longest_line = line;
		} else
			free (line);
	}

	if (longest_line) {
		printf ("The longest line (%d characters) is:\n %s\n", (int) max_len, longest_line);
		free (longest_line);
	}

	return 0;
}
