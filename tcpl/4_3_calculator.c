/*
 * A Polish notation calculator
 */

#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include "utils.h"
#include "stack.h"

typedef struct {
	int type;
	double val;
	size_t mem;
} token_t;

enum tokens {
	TOK_INVALID, TOK_EOT, TOK_VALUE,
	TOK_PLUS, TOK_MINUS, TOK_MULT, TOK_DIV, TOK_MOD,
	TOK_SIN, TOK_EXP, TOK_POW,
	TOK_DUP, TOK_SWAP, TOK_MEM_SAVE, TOK_MEM_LOAD
};

static bool handle_token (double_stack_t *, double *, const token_t *);
static void get_next_token (const char *, token_t *);
static bool pop_2op (double_stack_t *, double *, double *);
static const char * extract_value (const char *, token_t *);

#define MEMORY_SLOTS ('Z' - 'A' + 1)

int main (void) {
	char * line = NULL;

	double_stack_t stack = double_stack_create ();
	double saved_values[MEMORY_SLOTS] = { 0.0 };

	while (x_getline (&line, stdin) != -1) {
		token_t token;

		get_next_token (line, &token);

		while (true) {
			if (!handle_token (&stack, saved_values, &token))
				break;

			get_next_token (NULL, &token);
		}

		free (line);
	}

	double_stack_delete (&stack);

	return 0;
}

static bool handle_token (double_stack_t * stack, double * saved_values, const token_t * token) {
	switch (token->type) {
		double op1 = 0.0;
		double op2 = 0.0;

		case TOK_INVALID:
			fprintf (stderr, "Malformed expression encountered\n");
			double_stack_purge (stack);
			return false;
		case TOK_EOT:
			if (double_stack_empty (stack))
				return false;

			double result = double_stack_pop (stack);

			if (!double_stack_empty (stack)) {
				fprintf (stderr, "Malformed expression encountered\n");
				double_stack_purge (stack);
				return false;
			}

			printf ("%.6f\n", result);
			return false;
		case TOK_VALUE:
			double_stack_push (stack, token->val);
			return true;
		case TOK_PLUS:
			if (!pop_2op (stack, &op1, &op2)) {
				fprintf (stderr, "Missing operand for +\n");
				return false;
			}

			double_stack_push (stack, op1 + op2);
			return true;
		case TOK_MINUS:
			if (!pop_2op (stack, &op1, &op2)) {
				fprintf (stderr, "Missing operand for -\n");
				return false;
			}

			double_stack_push (stack, op1 - op2);
			return true;
		case TOK_MULT:
			if (!pop_2op (stack, &op1, &op2)) {
				fprintf (stderr, "Missing operand for *\n");
				return false;
			}

			double_stack_push (stack, op1 * op2);
			return true;
		case TOK_DIV:
			if (!pop_2op (stack, &op1, &op2)) {
				fprintf (stderr, "Missing operand for /\n");
				return false;
			} else if (ABS (op2) < EPS) {
				fprintf (stderr, "Division by zero\n");
				return false;
			}

			double_stack_push (stack, op1 / op2);
			return true;
		case TOK_MOD:
			if (!pop_2op (stack, &op1, &op2)) {
				fprintf (stderr, "Missing operand for %%\n");
				return false;
			} else if (ABS (op2) < EPS) {
				fprintf (stderr, "Division by zero\n");
				return false;
			}

			int res = (int) op1 % (int) op2;

			double_stack_push (stack, res);
			return true;
		case TOK_SWAP:
			if (!pop_2op (stack, &op1, &op2)) {
				fprintf (stderr, "Missing operand for swap\n");
				return false;
			}

			double_stack_push (stack, op2);
			double_stack_push (stack, op1);
			return true;
		case TOK_POW:
			if (!pop_2op (stack, &op1, &op2)) {
				fprintf (stderr, "Missing operand for pow\n");
				return false;
			}

			double_stack_push (stack, pow (op1, op2));
			return true;
		case TOK_DUP:
			if (double_stack_empty (stack)) {
				fprintf (stderr, "Missing operand for dup\n");
				return false;
			}

			double_stack_push (stack, double_stack_top (stack));
			return true;
		case TOK_EXP:
			if (double_stack_empty (stack)) {
				fprintf (stderr, "Missing operand for exp\n");
				return false;
			}

			double_stack_push (stack, exp (double_stack_pop (stack)));
			return true;
		case TOK_SIN:
			if (double_stack_empty (stack)) {
				fprintf (stderr, "Missing operand for sin\n");
				return false;
			}

			double_stack_push (stack, sin (double_stack_pop (stack)));
			return true;
		case TOK_MEM_SAVE:
			if (token->mem < MEMORY_SLOTS) {
				double val = 0.0;

				if (!double_stack_empty (stack))
					val = double_stack_top (stack);

				saved_values[token->mem] = val;
			}

			return true;
		case TOK_MEM_LOAD:
			if (token->mem < MEMORY_SLOTS)
				double_stack_push (stack, saved_values[token->mem]);

			return true;
		default:
			return false;
	}
}

static bool pop_2op (double_stack_t * stack, double * op1, double * op2) {
	if (!double_stack_empty (stack))
		*op2 = double_stack_pop (stack);
	else
		*op2 = 0.0;

	if (!double_stack_empty (stack))
		*op1 = double_stack_pop (stack);
	else {
		*op1 = 0.0;
		double_stack_purge (stack);
		return false;
	}

	return true;
}

static const char * extract_value (const char * s, token_t * t) {
	char * end_ptr = NULL;
	double v = strtod (s, &end_ptr);

	if (s == end_ptr) {
		t->type = TOK_INVALID;
		return s + 1;
	} else {
		t->type = TOK_VALUE;
		t->val = v;
		return end_ptr;
	}
}

static void get_next_token (const char * str, token_t * t) {
	static const char * s = NULL;

	t->type = TOK_INVALID;
	t->val = 0.0;
	t->mem = 0;

	if (str)
		s = str;

	if (!s)
		return;

	while (isspace (*s))
		s++;

	if (isdigit (*s) || *s == '.')
		s = extract_value (s, t);
	else if (*s == '-') {
		if (isspace (s[1]) || s[1] == '\0') {
			t->type = TOK_MINUS;
			s++;
		} else
			s = extract_value (s, t);
	} else if (islower (*s)) {
		if (!strncmp (s, "dup", 3)) {
			t->type = TOK_DUP;
			s += 3;
		} else if (!strncmp (s, "swap", 4)) {
			t->type = TOK_SWAP;
			s += 4;
		} else if (!strncmp (s, "sin", 3)) {
			t->type = TOK_SIN;
			s += 3;
		} else if (!strncmp (s, "exp", 3)) {
			t->type = TOK_EXP;
			s += 3;
		} else if (!strncmp (s, "pow", 3)) {
			t->type = TOK_POW;
			s += 3;
		} else {
			t->type = TOK_INVALID;
			s++;
		}
	} else if (isupper (*s)) {
		t->type = TOK_MEM_LOAD;
		t->mem = *s - 'A';
		s++;
	} else if (*s == '&') {
		if (isupper (s[1])) {
			t->type = TOK_MEM_SAVE;
			t->mem = s[1] - 'A';
			s += 2;
		} else {
			t->type = TOK_INVALID;
			s++;
		}
	} else if (*s == '+') {
		t->type = TOK_PLUS;
		s++;
	} else if (*s == '*') {
		t->type = TOK_MULT;
		s++;
	} else if (*s ==  '/') {
		t->type = TOK_DIV;
		s++;
	} else if (*s == '%') {
		t->type = TOK_MOD;
		s++;
	} else if (*s == '\0') {
		t->type = TOK_EOT;
	} else {
		t->type = TOK_INVALID;
		s++;
	}
}
