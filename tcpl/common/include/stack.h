#ifndef STACK_H
#define STACK_H

#include <stdlib.h>
#include <stdbool.h>

typedef struct {
	size_t allocated;
	size_t used;
	int * payload;
} int_stack_t;

typedef struct {
	size_t allocated;
	size_t used;
	double * payload;
} double_stack_t;

int_stack_t int_stack_create (void);
void int_stack_delete (int_stack_t *);
void int_stack_push (int_stack_t *, int);
int int_stack_pop (int_stack_t *);
bool int_stack_empty (const int_stack_t *);

double_stack_t double_stack_create (void);
void double_stack_delete (double_stack_t *);
void double_stack_purge (double_stack_t *);
void double_stack_push (double_stack_t *, double);
double double_stack_pop (double_stack_t *);
double double_stack_top (double_stack_t *);
bool double_stack_empty (const double_stack_t *);

#endif
