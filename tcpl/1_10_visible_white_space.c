/*
 * Copy stdin to stdout replacing tabs with \t and backspace with \b
 */

#include <stdio.h>

int main () {
	int c = 0;

	while ((c = getchar ()) != EOF) {
		switch (c) {
			case '\t':
				printf ("\\t");
				break;
			case '\b':
				printf ("\\b");
				break;
			case '\\':
				printf ("\\\\");
				break;
			default:
				putchar (c);
				break;
		}
	}

	return 0;
}
