#include <stdio.h>

#define LOWER	-100
#define UPPER	200
#define STEP	10

int main () {
	printf ("%10s   %10s\n", "Celsius", "Fahrenheit");
	printf ("%10s---%10s\n", "-------", "----------");

	for (int celsius = LOWER; celsius <= UPPER; celsius += STEP) {
		double fahrenheit = (9.0 / 5.0 * celsius) + 32.0;
		printf ("%10d   %10.1f\n", celsius, fahrenheit);
	}

	return 0;
}
