/*
 * Print a histogram of stdin word lengths
 */

#include <unistd.h>
#include <stdio.h>
#include <stdbool.h>
#include <ctype.h>
#include "utils.h"

#define MAX_LEN		30
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

	int lengths[MAX_LEN + 1] = { 0 };

	int max_length = 0;
	int length = 0;
	int c = 0;

	while ((c = getchar ()) != EOF) {
		if (isspace (c)) {
			if (length > 0) {
				if (length > MAX_LEN)
					length = MAX_LEN;

				if (length > max_length)
					max_length = length;

				lengths[length] += 1;

				length = 0;
			}
		} else
			length++;
	}

	print_histogram (lengths, max_length + 1, vertical, vertical ? VERTICAL_SIZE : HORIZONTAL_SIZE);

	return 0;
}
