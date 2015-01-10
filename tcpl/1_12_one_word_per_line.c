/*
 * Copy stdin to stdout one word per line
 */

#include <stdio.h>
#include <ctype.h>
#include <stdbool.h>

int main () {
	bool in_word = false;

	int c = 0;

	while ((c = getchar ()) != EOF)
		if (isspace (c)) {
			if (in_word) {
				in_word = false;
				putchar ('\n');
			}
		} else {
			in_word = true;
			putchar (c);
		}

	return 0;
}
