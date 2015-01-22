/*
 * Print built-in data type limits
 */

#include <stdint.h>
#include <stdio.h>
#include <limits.h>
#include <float.h>
#include <stdbool.h>
#include <math.h>

// Assumes two's complement representation of signed types
#define SIGNED_MIN(v) for (v = 1; v > 0; v <<= 1);
#define SIGNED_MAX(v) do { \
		SIGNED_MIN (v); \
		v = ~v; \
	} while (false);

// Assumes IEEE-754 floating point formats
static float float_min (void);
static double double_min (void);
static long double long_double_min (void);

typedef struct {
	unsigned char uchar_min;
	unsigned char uchar_max;
	signed char char_min;
	signed char char_max;
	unsigned int uint_min;
	unsigned int uint_max;
	signed int int_min;
	signed int int_max;
	unsigned long ulong_min;
	unsigned long ulong_max;
	signed long long_min;
	signed long long_max;
	float flt_min;
	float flt_max;
	double dbl_min;
	double dbl_max;
	long double ldbl_min;
	long double ldbl_max;
} limits_t;

static void print_system_limits (void);
static void print_report (const limits_t *);

int main (void) {
	print_system_limits ();

	return 0;
}

static void print_system_limits (void) {
	printf ("Read from system headers:\n\n");

	limits_t limits;

	limits.uchar_min = 0;
	limits.uchar_max = UCHAR_MAX;
	limits.char_min = CHAR_MIN;
	limits.char_max = CHAR_MAX;
	limits.uint_min = 0;
	limits.uint_max = UINT_MAX;
	limits.int_min = INT_MIN;
	limits.int_max = INT_MAX;
	limits.ulong_min = 0;
	limits.ulong_max = ULONG_MAX;
	limits.long_min = LONG_MIN;
	limits.long_max = LONG_MAX;
	limits.flt_min = -FLT_MAX;
	limits.flt_max = FLT_MAX;
	limits.dbl_min = -DBL_MAX;
	limits.dbl_max = DBL_MAX;
	limits.ldbl_min = -LDBL_MAX;
	limits.ldbl_max = LDBL_MAX;

	print_report (&limits);

	printf ("\nCalculated:\n\n");

	limits.uchar_min = 0;
	limits.uchar_max = ~0;
	SIGNED_MIN (limits.char_min);
	SIGNED_MAX (limits.char_max);
	limits.uint_min = 0;
	limits.uint_max = ~0;
	SIGNED_MIN (limits.int_min);
	SIGNED_MAX (limits.int_max);
	limits.ulong_min = 0;
	limits.ulong_max = ~0L;
	SIGNED_MIN (limits.long_min);
	SIGNED_MAX (limits.long_max);
	limits.flt_min = float_min ();
	limits.flt_max = -limits.flt_min;
	limits.dbl_min = double_min ();
	limits.dbl_max = -limits.dbl_min;
	limits.ldbl_min = long_double_min ();
	limits.ldbl_max = -limits.ldbl_min;

	print_report (&limits);
}

static float float_min (void) {
	union {
		uint32_t bits;
		float f;
	} float_repr;

	float_repr.bits = ~0;
	float_repr.bits &= ~(1 << 23);

	return float_repr.f;
}

static double double_min (void) {
	union {
		uint64_t bits;
		double d;
	} double_repr;

	double_repr.bits = ~0;
	double_repr.bits &= ~(1UL << 52);

	return double_repr.d;
}

static long double long_double_min (void) {
	union {
		uint64_t bits[2];
		long double d;
	} long_double_repr;

	long_double_repr.bits[0] = ~0;
	long_double_repr.bits[1] = ~1UL;

	return long_double_repr.d;
}

static void print_report (const limits_t * limits) {
	printf (" %-30s%u\n", "Lowest unsigned char", limits->uchar_min);
	printf (" %-30s%u\n", "Highest unsigned char", limits->uchar_max);

	putchar ('\n');

	printf (" %-30s%d\n", "Lowest signed char", limits->char_min);
	printf (" %-30s%d\n", "Highest signed char", limits->char_max);

	putchar ('\n');

	printf (" %-30s%u\n", "Lowest unsigned int", limits->uint_min);
	printf (" %-30s%u\n", "Highest unsigned int", limits->uint_max);

	putchar ('\n');

	printf (" %-30s%d\n", "Lowest signed int", limits->int_min);
	printf (" %-30s%d\n", "Highest signed int", limits->int_max);

	putchar ('\n');

	printf (" %-30s%lu\n", "Lowest unsigned long", limits->ulong_min);
	printf (" %-30s%lu\n", "Highest unsigned long", limits->ulong_max);

	putchar ('\n');

	printf (" %-30s%ld\n", "Lowest signed long", limits->long_min);
	printf (" %-30s%ld\n", "Highest signed long", limits->long_max);

	putchar ('\n');

	printf (" %-30s%e\n", "Lowest float", limits->flt_min);
	printf (" %-30s%e\n", "Highest float", limits->flt_max);

	putchar ('\n');

	printf (" %-30s%e\n", "Lowest double", limits->dbl_min);
	printf (" %-30s%e\n", "Highest double", limits->dbl_max);

	putchar ('\n');

	printf (" %-30s%Le\n", "Lowest long double", limits->ldbl_min);
	printf (" %-30s%Le\n", "Highest long double", limits->ldbl_max);
}
