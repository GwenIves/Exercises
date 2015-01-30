/*
 * Replace spaces on stdin with tabs
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include "tcpl_utils.h"

#define DEFAULT_TABSIZE	8

static void print_tabs (int, int, int, int *);

int main (int argc, char ** argv) {
	int tabsize = DEFAULT_TABSIZE;
	int * tablist = NULL;

	int arg = 0;

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

	bool in_spaces = false;

	int column = 0;
	int spaces_start = 0;

	int c = 0;

	while ((c = getchar ()) != EOF) {
		if (c == ' ') {
			if (!in_spaces) {
				in_spaces = true;
				spaces_start = column;
			}

			column++;
		} else {
			if (in_spaces && column == spaces_start + 1) {
				putchar (' ');
				in_spaces = false;
			} else if (in_spaces) {
				print_tabs (spaces_start, column, tabsize, tablist);
				in_spaces = false;
			}

			putchar (c);

			if (c == '\n')
				column = 0;
			else
				column++;
		}
	}

	free (tablist);

	return 0;
}

static void print_tabs (int spaces_start, int column, int tabsize, int * tablist) {
	if (tablist) {
		for (size_t i = 0; tablist[i] != -1; i++) {
			if (spaces_start > tablist[i])
				continue;
			else if (column < tablist[i])
				break;
			else {
				putchar ('\t');
				spaces_start = tablist[i];
			}
		}
	}

	int tab_start = spaces_start / tabsize;
	int tab_stop = column / tabsize;

	if (tab_start < tab_stop)
		spaces_start = tab_start * tabsize;

	while (spaces_start + tabsize <= column) {
		putchar ('\t');
		spaces_start += tabsize;
	}

	while (spaces_start < column) {
		putchar (' ');
		spaces_start++;
	}
}
