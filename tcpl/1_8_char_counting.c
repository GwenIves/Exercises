/*
 * Count the number of tabs, blanks and newlines on stdin
 */

#include <stdio.h>

int main (void) {
	int tabs = 0;
	int blanks = 0;
	int newlines = 0;

	int c = 0;

	while ((c = getchar ()) != EOF)
		switch (c) {
			case ' ':
				blanks++;
				break;
			case '\t':
				tabs++;
				break;
			case '\n':
				newlines++;
				break;
			default:
				break;
		}

	printf ("Tabs: %d\n", tabs);
	printf ("Blanks: %d\n", blanks);
	printf ("Newlines: %d\n", newlines);

	return 0;
}
