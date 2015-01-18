#ifndef STACK_H
#define STACK_H

#include <stdlib.h>
#include <stdbool.h>

typedef struct {
	size_t allocated;
	size_t used;
	int * payload;
} int_stack_t;

int_stack_t int_stack_create (void);
void int_stack_delete (int_stack_t *);
void int_stack_push (int_stack_t *, int);
int int_stack_pop (int_stack_t *);
bool int_stack_empty (int_stack_t *);

#endif
