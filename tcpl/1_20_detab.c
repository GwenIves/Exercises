/*
 * Replace tabs on stdin with spaces
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "tcpl_utils.h"

#define DEFAULT_TABSIZE	8

static int print_spaces (int, int, int *);

int main (int argc, char ** argv) {
	int column = 0;
	int c = 0;

	int arg = 0;

	int tabsize = DEFAULT_TABSIZE;
	int * tablist = NULL;

	while ((arg = getopt (argc, argv, "m:M:")) != -1) {
		switch (arg) {
			int val = 0;

			case 'm':
				val = atoi (optarg);

				if (val > 0)
					tabsize = val;

				break;
			case 'M':
				tablist = get_tablist (optarg);
				break;
			case '?':
			default:
				break;
		}
	}

	while ((c = getchar ()) != EOF) {
		if (c == '\t') {
			column = print_spaces (column, tabsize, tablist);
		} else if (c == '\n') {
			putchar (c);
			column = 0;
		} else {
			putchar (c);
			column++;
		}
	}

	free (tablist);

	return 0;
}

static int print_spaces (int column, int tabsize, int * tabstops) {
	if (tabstops) {
		int tabstop = 0;

		while ((tabstop = *tabstops++) != -1) {
			if (column >= tabstop)
				continue;
			else {
				while (column++ < tabstop)
					putchar (' ');

				return column;
			}
		}
	}

	do {
		putchar (' ');
	} while (++column % tabsize != 0);

	return column;
}
