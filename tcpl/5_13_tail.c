/*
 * Print only the last N lines of stdin, N is a single command line parameter
 */

#include <stdio.h>
#include <stdlib.h>
#include "utils.h"

static char ** allocate_buffer (int);

int main (int argc, char ** argv) {
	if (argc != 2)
		return 1;

	int N = atoi (argv[1]);

	if (N <= 0)
		return 1;

	char ** lines = allocate_buffer (N);

	int top = 0;
	char * line = NULL;

	while ((x_getline (&line, stdin)) != -1) {
		free (lines[top]);
		lines[top] = line;

		top = (top + 1) % N;
	}

	int start = 0;

	// Circular buffer wrapped around at least once
	if (lines[top])
		start = top;

	while (lines[start]) {
		printf ("%s\n", lines[start]);

		free (lines[start]);
		lines[start] = NULL;

		start = (start + 1) % N;
	}

	free (lines);

	return 0;
}

static char ** allocate_buffer (int lines_count) {
	char ** lines = x_malloc (lines_count * sizeof (char *));

	for (int i = 0; i < lines_count; i++)
		lines[i] = NULL;

	return lines;
}
