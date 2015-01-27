#include "stack.h"
#include "utils.h"

int_stack_t int_stack_create (void) {
	int_stack_t stack;

	stack.allocated = 0;
	stack.used = 0;
	stack.payload = NULL;

	return stack;
}

void int_stack_delete (int_stack_t * stack) {
	free (stack->payload);
}

void int_stack_push (int_stack_t * stack, int data) {
	if (stack->used >= stack->allocated) {
		stack->allocated += 1;
		stack->allocated *= 2;

		stack->payload = x_realloc (stack->payload, stack->allocated * sizeof (int));
	}

	stack->payload[stack->used++] = data;
}

int int_stack_pop (int_stack_t * stack) {
	return stack->payload[--stack->used];
}

bool int_stack_empty (const int_stack_t * stack) {
	return stack->used == 0;
}

double_stack_t double_stack_create (void) {
	double_stack_t stack;

	stack.allocated = 0;
	stack.used = 0;
	stack.payload = NULL;

	return stack;
}

void double_stack_delete (double_stack_t * stack) {
	free (stack->payload);
}

void double_stack_purge (double_stack_t * stack) {
	stack->used = 0;
}

void double_stack_push (double_stack_t * stack, double data) {
	if (stack->used >= stack->allocated) {
		stack->allocated += 1;
		stack->allocated *= 2;

		stack->payload = x_realloc (stack->payload, stack->allocated * sizeof (double));
	}

	stack->payload[stack->used++] = data;
}

double double_stack_pop (double_stack_t * stack) {
	return stack->payload[--stack->used];
}

double double_stack_top (double_stack_t * stack) {
	return stack->payload[stack->used - 1];
}

bool double_stack_empty (const double_stack_t * stack) {
	return stack->used == 0;
}
