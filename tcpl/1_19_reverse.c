/*
 * Print stdin reversed lined by line
 */

#include <stdlib.h>
#include "utils.h"

static void reverse (char *, size_t len);

int main () {
	char * line = NULL;
	ssize_t len = 0;

	while ((len = x_getline (&line, stdin)) != -1) {
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
		char temp = line[start];

		line[start] = line[end];
		line[end] = temp;

		start++;
		end--;
	}
}
