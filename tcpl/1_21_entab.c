/*
 * Replace spaces on stdin with tabs
 */

#include <stdio.h>
#include <stdbool.h>

#define TABSIZE	8

int main (void) {
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
			if (in_spaces) {
				int tab_start = spaces_start / TABSIZE;
				int tab_stop = column / TABSIZE;

				if (tab_start < tab_stop)
					spaces_start = tab_start * TABSIZE;

				while (spaces_start + TABSIZE <= column) {
					putchar ('\t');
					spaces_start += TABSIZE;
				}

				while (spaces_start < column) {
					putchar (' ');
					spaces_start++;
				}

				in_spaces = false;
			}

			putchar (c);

			if (c == '\n')
				column = 0;
			else
				column++;
		}
	}

	return 0;
}
