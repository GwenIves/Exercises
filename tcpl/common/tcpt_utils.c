#include "tcpl_utils.h"

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
