/*
 * Binary search benchmark
 */

#include <stdlib.h>
#include <stdio.h>
#include "utils.h"

#define COMPUTATIONS	100000
#define ARRAY_SIZE	100000

static int bsearch_2cmp (int, int *, int);
static int bsearch_1cmp (int, int *, int);
static int * get_array (size_t);

int main (void) {
	struct timeval stamp1, stamp2, stamp3, stamp4;

	int * array = get_array (ARRAY_SIZE);

	x_gettimeofday (&stamp1);

	for (size_t i = 0; i < COMPUTATIONS; i++)
		bsearch_2cmp (rand (), array, ARRAY_SIZE);

	x_gettimeofday (&stamp2);

	free (array);

	array = get_array (ARRAY_SIZE);

	x_gettimeofday (&stamp3);

	for (size_t i = 0; i < COMPUTATIONS; i++)
		bsearch_1cmp (rand (), array, ARRAY_SIZE);

	x_gettimeofday (&stamp4);

	struct timeval diff_2cmp = time_diff (&stamp1, &stamp2);
	struct timeval diff_1cmp = time_diff (&stamp3, &stamp4);

	printf ("2 comparisons %7ld seconds, %7ld microseconds\n", diff_2cmp.tv_sec, diff_2cmp.tv_usec);
	printf ("1 comparison  %7ld seconds, %7ld microseconds\n", diff_1cmp.tv_sec, diff_1cmp.tv_usec);

	free (array);

	return 0;
}

static int * get_array (size_t size) {
	int * a = x_malloc (size * sizeof (int));

	for (size_t i = 0; i < size; i++)
		a[i] = rand ();

	qsort (a, size, sizeof (int), int_cmp);

	return a;
}

static int bsearch_2cmp (int x, int * array, int size) {
	int low = 0;
	int high = size - 1;

	while (low <= high) {
		int mid = (low + high) / 2;

		if (x < array[mid])
			high = mid - 1;
		else if (x > array[mid])
			low = mid + 1;
		else
			return mid;
	}

	return -1;
}

static int bsearch_1cmp (int x, int * array, int size) {
	int low = 0;
	int high = size - 1;

	while (low < high) {
		int mid = (low + high) / 2;

		if (x <= array[mid])
			high = mid;
		else
			low = mid + 1;
	}

	if (x == array[low])
		return low;
	else
		return -1;
}
