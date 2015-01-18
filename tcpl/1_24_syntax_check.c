/*
 * Check C source code for matching parentheses, brackets and braces
 */

#include <stdio.h>
#include <stdbool.h>
#include "stack.h"
#include "tcpl_utils.h"

static bool check_braces (int_stack_t *, int);

int main (void) {
	int c = 0;
	int lineno = 1;

	int_stack_t braces = int_stack_create ();

	int state = CODE;

	while ((c = getchar ()) != EOF) {
		if (c == '\n')
			lineno++;

		if (state == CODE && !check_braces (&braces, c)) {
			fprintf (stderr, "Unmatched %c on line %d\n", (char) c, lineno);
			break;
		}

		state = c_parse_next_state (state, c);
	}

	if (!int_stack_empty (&braces))
		fprintf (stderr, "Unexpected end of file\n");

	int_stack_delete (&braces);

	return 0;
}

static bool check_braces (int_stack_t * braces, int c) {
	switch (c) {
		case '(':
		case '[':
		case '{':
			int_stack_push (braces, c);
			return true;
		case ')':
		case ']':
		case '}':
			if (int_stack_empty (braces))
				return false;

			int prev = int_stack_pop (braces);

			if (prev == '(' && c == ')')
				return true;
			else if (prev == '[' && c == ']')
				return true;
			else if (prev == '{' && c == '}')
				return true;
			else
				return false;
		default:
			return true;
	}
}
