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
