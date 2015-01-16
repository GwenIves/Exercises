/*
 * Replace tabs on stdin with spaces
 */

#include <stdio.h>

#define TABSIZE	8

int main (void) {
	int column = 0;
	int c = 0;

	while ((c = getchar ()) != EOF) {
		if (c == '\t') {
			do {
				putchar (' ');
				column++;
			} while (column % TABSIZE != 0);
		} else if (c == '\n') {
			putchar (c);
			column = 0;
		} else {
			putchar (c);
			column++;
		}
	}

	return 0;
}
