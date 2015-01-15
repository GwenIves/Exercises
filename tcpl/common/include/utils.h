#ifndef UTILS_H
#define UTILS_H

#include <stdio.h>
#include <stdbool.h>

ssize_t x_getline (char **, FILE *);

void print_histogram (int *, size_t, bool, int);

#endif
