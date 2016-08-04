#!/bin/env python3

import re

from ply import lex, yacc

text = """
@Book{blanchette+summerfield,
  author    =  "Jasmin Blanchette and Mark Summerfield",
  title     =  "C++ GUI Programming with Qt 4,
                Second Edition",
  publisher =   "Prentice Hall",
  year      =   2008,
  address   =  "New York"
}
@Book{abramowitz+stegun,
  author    =     "Milton {Abramowitz} and Irene A. {Stegun}"
}
@Book{hicks2001
}
"""

def main():
    re_whitespace = re.compile(r'\s+')

    tokens = (
        "RECORD_START",
        "RECORD_END",
        "KEY",
        "STRING",
        "INTEGER",
        "COMMA",
        "EQUALS"
    )

    def t_RECORD_START(t):
        r"@Book{[^,}]+"
        t.value = t.value[6:].strip()
        return t

    def t_RECORD_END(t):
        r"}"
        return t

    def t_KEY(t):
        r"[a-zA-Z]\w*"
        return t

    def t_STRING(t):
        r'"[^"]*"'
        t.value = re_whitespace.sub(' ', t.value)
        return t

    def t_INTEGER(t):
        r"\d+"
        t.value = int(t.value)
        return t

    def t_COMMA(t):
        r","
        return t

    def t_EQUALS(t):
        r"="
        return t

    t_ignore = " \t"

    def t_newline(t):
        r"\n"
        t.lexer.lineno += len(t.value)

        return None

    def t_error(t):
        line = t.value.strip()

        i = line.find('\n')
        if i != -1:
            line[:i]

        print("Failed to parse line {}: {}".format(t.lineno + 1, line))
        return None

    def p_booklist(p):
        """BOOKLIST :
        | BOOK BOOKLIST"""
        p_len = len(p)

        if p_len == 1:
            p[0] = []
        else:
            p[0] = [p[1]] + p[2]

    def p_book(p):
        """BOOK : RECORD_START RECORD_END
        | RECORD_START COMMA PROPLIST RECORD_END"""
        if len(p) == 3:
            p[0] = [p[1], dict()]
        else:
            p[0] = [p[1], dict(p[3])]

    def p_proplist(p):
        """PROPLIST :
        | PROPERTY
        | PROPERTY COMMA PROPLIST"""
        p_len = len(p)

        if p_len == 1:
            p[0] = []
        elif p_len == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_property(p):
        """PROPERTY : KEY EQUALS STRING
        | KEY EQUALS INTEGER"""
        p[0] = [p[1], p[3]]

    def p_error(p):
        if p is None:
            msg = "Unknown error"
        else:
            msg = "Syntax error, line {}: {}".format(p.lineno + 1, p.type)

        raise ValueError(msg)

    lexer = lex.lex(debug=False)
    parser = yacc.yacc()

    try:
        parsed = dict(parser.parse(text, lexer=lexer))
    except ValueError as err:
        print(err)
        parsed = {}

    print(parsed)

if __name__ == '__main__':
    main()
