/*
 * Various string handling routines driver program
 */

#include <stdio.h>
#include <string.h>
#include <stdbool.h>

static void strend_test (const char *, const char *);
static bool strend (const char *, const char *);
static void strncpy_test (const char *, size_t);
static void x_strncpy (char *, const char *, size_t);
static void strncat_test (const char *, const char *, size_t);
static void x_strncat (char *, const char *, size_t);
static void strncmp_test (const char *, const char *, size_t);
static int x_strncmp (const char *, const char *, size_t);

int main (void) {
	strend_test ("hello", "bye");
	strend_test ("bye", "hello");
	strend_test ("hello, world", "world");
	strend_test ("hello, world", "hello");

	putchar ('\n');

	strncpy_test ("hello world", 100);
	strncpy_test ("hello world", 12);
	strncpy_test ("hello world", 11);
	strncpy_test ("hello world", 5);

	putchar ('\n');

	strncat_test ("hello ", "world", 100);
	strncat_test ("hello ", "world", 5);
	strncat_test ("hello ", "world", 4);
	strncat_test ("hello ", "world", 1);
	strncat_test ("hello ", "world", 0);

	putchar ('\n');

	strncmp_test ("hello", "hello world", 10);
	strncmp_test ("hello", "hello world", 6);
	strncmp_test ("hello", "hello world", 5);
	strncmp_test ("hello", "hello world", 4);
	strncmp_test ("hello", "hello world", 0);

	return 0;
}

static void strend_test (const char * str, const char * tail) {
	printf ("strend (%s, %s) = %d\n", str, tail, (int) strend (str, tail));
}

static bool strend (const char * str, const char * tail) {
	size_t str_len = strlen (str);
	size_t tail_len = strlen (tail);

	if (tail_len > str_len)
		return false;
	else if (strcmp (tail, str + str_len - tail_len) == 0)
		return true;
	else
		return false;
}

static void strncpy_test (const char * str, size_t size) {
	if (size == 0)
		return;

	char buffer[size];

	x_strncpy (buffer, str, size);

	buffer[size - 1] = '\0';

	printf ("strncpy (%s, %lu) = \"%s\"\n", str, size, buffer);
}

static void x_strncpy (char * dst, const char * src, size_t size) {
	while (size-- > 0 && (*dst++ = *src++) != '\0')
		;
}

static void strncat_test (const char * dst, const char * src, size_t size) {
	char buffer[strlen (dst) + size + 1];

	strcpy (buffer, dst);
	x_strncat (buffer, src, size);

	printf ("strncat (%s %s, %lu) = \"%s\"\n", dst, src, size, buffer);
}

static void x_strncat (char * dst, const char * src, size_t size) {
	while (*dst)
		dst++;

	while (size-- > 0 && *src != '\0')
		*dst++ = *src++;

	*dst = '\0';
}

static void strncmp_test (const char * a, const char * b, size_t size) {
	printf ("strncmp (%s, %s, %lu) = %d\n", a, b, size, x_strncmp (a, b, size));
}

static int x_strncmp (const char * a, const char * b, size_t size) {
	if (size == 0)
		return 0;

	for (; *a == *b; a++, b++)
		if (--size == 0 || *a == '\0')
			return 0;

	return *a - *b;
}
