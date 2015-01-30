#ifndef TCPL_UTILS_H
#define TCPL_UTILS_H

enum c_parse_states {BLOCK_COMMENT, LINE_COMMENT, SLASH, STAR, ESCAPE_CHAR, ESCAPE_STRING, CHAR, STRING, CODE};

int c_parse_next_state (int, int);
int * get_tablist (char *);

#endif
