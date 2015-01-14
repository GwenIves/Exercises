/*
 * Print a histogram of stdin character frequencies
 */

#include <unistd.h>
#include <stdio.h>
#include <stdbool.h>
#include <ctype.h>
#include "utils.h"

#define CHAR_COUNT	26
#define HORIZONTAL_SIZE	100
#define VERTICAL_SIZE	40

int main (int argc, char ** argv) {
	bool vertical = false;

	int arg = 0;

	while ((arg = getopt (argc, argv, "v")) != -1) {
		switch (arg) {
			case 'v':
				vertical = true;
				break;
			case '?':
			default:
				break;
		}
	}

	int frequencies[CHAR_COUNT] = { 0 };

	int c = 0;

	while ((c = getchar ()) != EOF) {
		int character = tolower (c);

		if (character >= 'a' && character <= 'z')
			frequencies[character - 'a'] += 1;
	}

	print_histogram (frequencies, CHAR_COUNT, vertical, vertical ? VERTICAL_SIZE : HORIZONTAL_SIZE);

	return 0;
}
