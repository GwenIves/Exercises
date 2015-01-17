/*
 * Remove comments from C source codes
 */

#include <stdio.h>

enum state {BLOCK_COMMENT, LINE_COMMENT, SLASH, STAR, ESCAPE_CHAR, ESCAPE_STRING, CHAR, STRING, CODE};

int main (void) {
	int c = 0;

	int state = CODE;

	while ((c = getchar ()) != EOF) {
		switch (state) {
			case BLOCK_COMMENT:
				if (c == '*')
					state = STAR;

				break;
			case STAR:
				if (c == '/')
					state = CODE;
				else
					state = BLOCK_COMMENT;

				break;
			case LINE_COMMENT:
				if (c == '\n') {
					putchar (c);
					state = CODE;
				}

				break;
			case CHAR:
				putchar (c);

				if (c == '\'')
					state = CODE;
				else if (c == '\\')
					state = ESCAPE_CHAR;

				break;
			case STRING:
				putchar (c);

				if (c == '"')
					state = CODE;
				else if (c == '\\')
					state = ESCAPE_STRING;

				break;
			case ESCAPE_CHAR:
				putchar (c);
				state = CHAR;

				break;
			case ESCAPE_STRING:
				putchar (c);
				state = STRING;

				break;
			case SLASH:
				if (c == '/')
					state = LINE_COMMENT;
				else if (c == '*')
					state = BLOCK_COMMENT;
				else {
					putchar ('/');
					putchar (c);

					if (c == '\'')
						state = CHAR;
					else if (c == '"')
						state = STRING;
					else
						state = CODE;
				}

				break;
			case CODE:
			default:
				if (c == '/') {
					state = SLASH;
				} else if (c == '\'') {
					putchar (c);
					state = CHAR;
				} else if (c == '"') {
					putchar (c);
					state = STRING;
				} else {
					putchar (c);
				}

				break;
		}
	}

	return 0;
}
