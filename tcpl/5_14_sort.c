/*
 * Sort lines on stdin
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>
#include <ctype.h>
#include "utils.h"

typedef struct {
	bool numeric;
	bool reverse;
	bool fold;
	bool directory;
} sort_options_t;

// External flag for strdircmp ()
static bool g_opts_fold;

static char ** read_lines (size_t *);
static void sort_lines (char **, size_t, sort_options_t *);
static void print_lines (char **, size_t);
static void free_lines (char **, size_t);
static void reverse_lines (char **, size_t);
static int numeric_str_cmp (const void *, const void *);
static int string_dir_cmp (const void *, const void *);
static int strdircmp (const char *, const char *);

int main (int argc, char ** argv) {
	int arg = 0;

	sort_options_t opts = {.numeric = false, .reverse = false, .fold = false, .directory = false};

	while ((arg = getopt (argc, argv, "fnrd")) != -1) {
		switch (arg) {
			case 'n':
				opts.numeric = true;
				break;
			case 'r':
				opts.reverse = true;
				break;
			case 'f':
				opts.fold = true;
				break;
			case 'd':
				opts.directory = true;
				break;
			case '?':
			default:
				break;
		}
	}

	size_t lines_count = 0;
	char ** lines = read_lines (&lines_count);

	sort_lines (lines, lines_count, &opts);
	print_lines (lines, lines_count);

	free_lines (lines, lines_count);

	return 0;
}

static char ** read_lines (size_t * count) {
	size_t used = 0;
	size_t allocated = 0;

	char ** lines = NULL;
	char * line = NULL;

	while ((x_getline (&line, stdin)) != -1) {
		if (used >= allocated) {
			allocated += 1;
			allocated *= 2;

			lines = x_realloc (lines, allocated * sizeof (char *));
		}

		lines[used++] = line;
	}

	*count = used;

	return lines;
}

static void sort_lines (char ** lines, size_t count, sort_options_t * opts) {
	if (opts->numeric)
		qsort (lines, count, sizeof (char *), numeric_str_cmp);
	else if (opts->directory) {
		g_opts_fold = opts->fold;
		qsort (lines, count, sizeof (char *), string_dir_cmp);
	} else if (opts->fold)
		qsort (lines, count, sizeof (char *), string_case_cmp);
	else
		qsort (lines, count, sizeof (char *), string_cmp);

	if (opts->reverse)
		reverse_lines (lines, count);
}

static void print_lines (char ** lines, size_t count) {
	for (size_t i = 0; i < count; i++)
		printf ("%s\n", lines[i]);
}

static void reverse_lines (char ** lines, size_t count) {
	if (count == 0)
		return;

	for (size_t i = 0, j = count - 1; i < j; i++, j--) {
		char * line = lines[i];
		lines[i] = lines[j];
		lines[j] = line;
	}
}

static void free_lines (char ** lines, size_t count) {
	for (size_t i = 0; i < count; i++)
		free (lines[i]);

	free (lines);
}

static int numeric_str_cmp (const void * a, const void * b) {
	double aa = atof (* ((const char **) a));
	double bb = atof (* ((const char **) b));

	if (aa > bb)
		return 1;
	else if (aa < bb)
		return -1;
	else
		return 0;
}

static int string_dir_cmp (const void * a, const void * b) {
	return strdircmp (* (char **) a, * (char **) b);
}

static int strdircmp (const char * a, const char * b) {
	size_t i = 0;
	size_t j = 0;

	while (true) {
		while (!isalpha (a[i]) && !isspace (a[i]) && a[i] != '\0')
			i++;

		while (!isalpha (b[j]) && !isspace (b[j]) && b[j] != '\0')
			j++;

		if (a[i] == '\0' || b[j] == '\0')
			return a[i] - b[j];
		else if (g_opts_fold && toupper (a[i]) != toupper (b[j]))
			return toupper (a[i]) - toupper (b[j]);
		else if (!g_opts_fold && a[i] != b[j])
			return a[i] - b[j];
		else {
			i++;
			j++;
		}
	}
}
