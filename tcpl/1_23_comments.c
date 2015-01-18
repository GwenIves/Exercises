/*
 * Remove comments from C source codes
 */

#include <stdio.h>
#include "tcpl_utils.h"

int main (void) {
	int c = 0;

	int state = CODE;

	while ((c = getchar ()) != EOF) {
		switch (state) {
			case LINE_COMMENT:
				if (c == '\n')
					putchar (c);

				break;
			case CHAR:
			case STRING:
			case ESCAPE_CHAR:
			case ESCAPE_STRING:
				putchar (c);

				break;
			case SLASH:
				if (c != '/' && c != '*') {
					putchar ('/');
					putchar (c);
				}

				break;
			case CODE:
				if (c != '/')
					putchar (c);

				break;
			case BLOCK_COMMENT:
			case STAR:
			default:
				break;
		}

		state = c_parse_next_state (state, c);
	}

	return 0;
}
