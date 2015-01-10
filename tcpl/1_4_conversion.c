/*
 * Print a table of temperatures in units of both Celsius and Fahrenheit
 */

#include <unistd.h>
#include <stdio.h>
#include <stdbool.h>

#define LOWER	-100
#define UPPER	200
#define STEP	10

static void print_temperatures (int);

int main (int argc, char ** argv) {
	bool reverse = false;

	int arg = 0;

	while ((arg = getopt (argc, argv, "r")) != -1) {
		switch (arg) {
			case 'r':
				reverse = true;
				break;
			case '?':
			default:
				break;
		}
	}

	printf ("%10s   %10s\n", "Celsius", "Fahrenheit");
	printf ("%10s---%10s\n", "-------", "----------");

	if (reverse) {
		for (int celsius = UPPER; celsius >= LOWER; celsius -= STEP)
			print_temperatures (celsius);
	} else {
		for (int celsius = LOWER; celsius <= UPPER; celsius += STEP)
			print_temperatures (celsius);
	}

	return 0;
}

static void print_temperatures (int celsius) {
	double fahrenheit = (9.0 / 5.0 * celsius) + 32.0;

	printf ("%10d   %10.1f\n", celsius, fahrenheit);
}
