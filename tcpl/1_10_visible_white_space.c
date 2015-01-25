/*
 * Copy stdin to stdout escaping/unescaping special characters
 */

#include <stdio.h>
#include <unistd.h>
#include <stdbool.h>

static void escape (int);
static void unescape (int);

int main (int argc, char ** argv) {
	bool should_escape = true;

	int arg = 0;

	while ((arg = getopt (argc, argv, "u")) != -1) {
		switch (arg) {
			case 'u':
				should_escape = false;
				break;
			case '?':
			default:
				break;
		}
	}

	int c = 0;

	if (should_escape) {
		while ((c = getchar ()) != EOF)
			escape (c);
	} else {
		while ((c = getchar ()) != EOF)
			unescape (c);
	}

	return 0;
}

static void escape (int c) {
	switch (c) {
		case '\t':
			printf ("\\t");
			break;
		case '\b':
			printf ("\\b");
			break;
		case '\n':
			printf ("\\n");
			break;
		case '\\':
			printf ("\\\\");
			break;
		default:
			putchar (c);
			break;
	}
}

static void unescape (int c) {
	static bool in_escape = false;

	if (in_escape) {
		switch (c) {
			case 't':
				putchar ('\t');
				break;
			case 'b':
				putchar ('\b');
				break;
			case 'n':
				putchar ('\n');
				break;
			case '\\':
				putchar ('\\');
				break;
			default:
				putchar (c);
				break;
		}

		in_escape = false;
	} else if (c == '\\')
		in_escape = true;
	else
		putchar (c);
}
