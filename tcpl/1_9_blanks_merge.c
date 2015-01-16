/*
 * Copy stdin to stdout replacing consecutive blanks with a single one
 */

#include <stdio.h>
#include <stdbool.h>

int main (void) {
	bool in_blanks = false;

	int c = 0;

	while ((c = getchar ()) != EOF) {
		if (c == ' ') {
			if (!in_blanks) {
				putchar (c);
				in_blanks = true;
			}
		} else {
			in_blanks = false;
			putchar (c);
		}
	}

	return 0;
}
