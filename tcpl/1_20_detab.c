/*
 * Replace tabs on stdin with spaces
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define DEFAULT_TABSIZE	8

int main (int argc, char ** argv) {
	int column = 0;
	int c = 0;

	int arg = 0;

	int tabsize = DEFAULT_TABSIZE;

	while ((arg = getopt (argc, argv, "m:")) != -1) {
		switch (arg) {
			int val = 0;

			case 'm':
				val = atoi (optarg);

				if (val > 0)
					tabsize = val;

				break;
			case '?':
			default:
				break;
		}
	}

	while ((c = getchar ()) != EOF) {
		if (c == '\t') {
			do {
				putchar (' ');
				column++;
			} while (column % tabsize != 0);
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
