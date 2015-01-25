/*
 * Expand a shorthand range notation given as a command line parameter into a complete list
 */

#include <stdio.h>
#include <stdbool.h>
#include <ctype.h>

static void expand (const char *);
static bool expand_range (const char *);

int main (int argc, char ** argv) {
	for (int i = 1; i < argc; i++)
		expand (argv[i]);

	return 0;
}

static void expand (const char * str) {
	const char * processed_up_to = NULL;

	while (*str != '\0') {
		bool status = expand_range (str);

		if (status) {
			str += 2;
			processed_up_to = str;
		} else {
			if (!processed_up_to || str > processed_up_to)
				putchar (*str);

			str++;
		}
	}

	putchar ('\n');
}

static bool expand_range (const char * str) {
	if (islower (str[0]) && str[1] == '-' && islower (str[2]))
		;
	else if (isupper (str[0]) && str[1] == '-' && isupper (str[2]))
		;
	else if (isdigit (str[0]) && str[1] == '-' && isdigit (str[2]))
		;
	else
		return false;

	if (str[0] > str[2])
		return false;

	for (char c = str[0]; c <= str[2]; c++)
		putchar (c);

	return true;
}
