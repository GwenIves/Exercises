#ifndef UTILS_H
#define UTILS_H

#include <stdio.h>
#include <stdbool.h>

ssize_t x_getline (char **, FILE *);
void * x_realloc (void *, size_t);

void print_histogram (const int *, size_t, bool, int);

#endif
