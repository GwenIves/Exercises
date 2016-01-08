#!/bin/env python3

def valid(string, chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
    passed = []

    for char in string:
        if char in chars:
            passed.append(char)

    return "".join(passed)

def charcount(text):
    counts = {}

    for char in text.lower():
        if char.isalpha():
            key = char
        elif char.isspace():
            key = "whitespace"
        else:
            key = "other"

        counts[key] = counts.get(key, 0) + 1

    return counts

def integer(val):
    try:
        val = float(val)
    except ValueError:
        return 0
    else:
        return round(val)

def increment_string(s):
    s = list(s.upper())
    last = len(s) - 1

    for i in range(last, -1, -1):
        if not s[i].isalpha():
            raise ValueError()
        elif s[i] == 'Z':
            continue
        else:
            s[i] = chr(ord(s[i]) + 1)

            for j in range(i + 1, last + 1):
                s[j] = 'A'

            break
    else:
        return 'A' * (last + 2)

    return "".join(s)

def leap_years(yearlist):
    def is_leap(year):
        if year % 400 == 0:
            return True
        elif year % 100 == 0:
            return False
        else:
            return year % 4 == 0

    for year in yearlist:
        if is_leap(year):
            yield year

def test_valid():
    assert valid("Barking!") == "B"
    assert valid("KL754", "0123456789") == "754"
    assert valid("BEAN", "abcdefghijklmnopqrstuvwxyz") == ""

def test_integer():
    assert integer(1) == 1
    assert integer("1") == 1
    assert integer(1.2) == 1
    assert integer("1.2") == 1
    assert integer("a") == 0

def test_increment():
    assert increment_string("A") == "B"
    assert increment_string("Z") == "AA"
    assert increment_string("AM") == "AN"
    assert increment_string("AZ") == "BA"
    assert increment_string("BA") == "BB"
    assert increment_string("BZ") == "CA"
    assert increment_string("ZZA") == "ZZB"
    assert increment_string("ZZZ") == "AAAA"
    assert increment_string("AAAA") == "AAAB"
    assert increment_string("AAAZ") == "AABA"

    try:
        increment_string("ABC2")
    except ValueError:
        pass
    else:
        assert False

def test_leap_years():
    leaps = list(leap_years([1600, 1604, 1700, 1704, 1800, 1900, 1996, 2000, 2004]))
    assert leaps == [1600, 1604, 1704, 1996, 2000, 2004]

def print_dict(d):
    def key(x):
        return (len(x), x)

    for k in sorted(d, key=key):
        print("{}: {}".format(k, d[k]))

def test_charcount():
    print_dict(charcount("Exceedingly Edible"))

def main():
    test_valid()
    test_charcount()
    test_integer()
    test_increment()
    test_leap_years()

if __name__ == '__main__':
    main()
