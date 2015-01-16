/*
 * Break long lines on stdin
 */

#include <stdlib.h>
#include <stdbool.h>
#include <ctype.h>
#include "utils.h"

#define MAX_LINE_LEN	80

static int find_line_break (char *, ssize_t, int);

int main (void) {
	char * line = NULL;
	ssize_t len = 0;

	while ((len = x_getline (&line, stdin)) != -1) {
		char * start = line;

		do {
			int line_size = find_line_break (start, len, MAX_LINE_LEN);

			printf ("%.*s\n", line_size, start);

			start += line_size;
			len -= line_size;
		} while (len > 0);

		free (line);
	}

	return 0;
}

static int find_line_break (char * line, ssize_t len, int max_size) {
	if (len <= max_size)
		return len;

	// If there is no blank before max_size, we will break inside a word
	int line_end = max_size;

	bool prev_blank = false;

	for (int i = 0; i <= max_size; i++) {
		if (isblank (line[i]))
			prev_blank = true;
		else if (prev_blank) {
			prev_blank = false;
			line_end = i;
		}
	}

	return line_end;
}
