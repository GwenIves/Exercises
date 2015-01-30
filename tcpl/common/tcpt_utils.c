#include <string.h>
#include <stdlib.h>
#include "tcpl_utils.h"
#include "utils.h"

int c_parse_next_state (int state, int c) {
	int new_state = state;

	switch (state) {
		case BLOCK_COMMENT:
			if (c == '*')
				new_state = STAR;

			break;
		case STAR:
			if (c == '/')
				new_state = CODE;
			else
				new_state = BLOCK_COMMENT;

			break;
		case LINE_COMMENT:
			if (c == '\n')
				new_state = CODE;

			break;
		case CHAR:
			if (c == '\'')
				new_state = CODE;
			else if (c == '\\')
				new_state = ESCAPE_CHAR;

			break;
		case STRING:
			if (c == '"')
				new_state = CODE;
			else if (c == '\\')
				new_state = ESCAPE_STRING;

			break;
		case ESCAPE_CHAR:
			new_state = CHAR;

			break;
		case ESCAPE_STRING:
			new_state = STRING;

			break;
		case SLASH:
			if (c == '/')
				new_state = LINE_COMMENT;
			else if (c == '*')
				new_state = BLOCK_COMMENT;
			else if (c == '\'')
				new_state = CHAR;
			else if (c == '"')
				new_state = STRING;
			else
				new_state = CODE;

			break;
		case CODE:
		default:
			if (c == '/')
				new_state = SLASH;
			else if (c == '\'')
				new_state = CHAR;
			else if (c == '"')
				new_state = STRING;
			else
				new_state = CODE;

			break;
	}

	return new_state;
}

// Parse a comma-separated tab-stops list. Returns an integer array terminated by -1
int * get_tablist (char * str) {
	size_t count = 0;

	int prev_val = 0;

	char * s_ptr = strtok (str, ",");

	do {
		int val = atoi (s_ptr);

		if (val > prev_val) {
			count++;
			prev_val = val;

			// Undo strtok modifications of str
			if (s_ptr > str)
				s_ptr[-1] = ',';
		} else
			break;
	} while ((s_ptr = strtok (NULL, ",")) != NULL);

	if (count == 0)
		return NULL;

	int * vals = x_malloc ((count + 1) * sizeof (int));

	s_ptr = strtok (str, ",");

	for (size_t i = 0; i < count; i++, s_ptr = strtok (NULL, ","))
		vals[i] = atoi (s_ptr);

	vals[count] = -1;

	return vals;
}
