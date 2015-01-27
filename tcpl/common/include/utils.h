#ifndef UTILS_H
#define UTILS_H

#include <sys/time.h>
#include <stdio.h>
#include <stdbool.h>

#define EPS	0.000001

#define ABS(x)	((x) < 0 ? -(x) : (x))

void x_gettimeofday (struct timeval *);
struct timeval time_diff (struct timeval *, struct timeval *);

ssize_t x_getline (char **, FILE *);
void * x_malloc (size_t);
void * x_realloc (void *, size_t);

int int_cmp (const void *, const void *);

void print_histogram (const int *, size_t, bool, int);

#endif
