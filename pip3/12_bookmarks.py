#!/usr/bin/env python3

import os
import pickle
import shelve
import sys

import Console

DISPLAY_LIMIT = 20

def main():
    filename = os.path.join(os.path.dirname(__file__), "bookmarks.dbm")

    functions = dict(
        a=add_bookmark,
        e=edit_bookmark,
        l=list_bookmarks,
        r=remove_bookmark,
        q=quit_
    )

    with shelve.open(filename, protocol=pickle.HIGHEST_PROTOCOL) as db:
        action = ""

        while True:
            print("\nBookmarks ({0})".format(os.path.basename(filename)))
            size = len(db)

            if action != "l" and 1 <= len(db) < DISPLAY_LIMIT:
                list_bookmarks(db)
            else:
                print("{0} bookmark{1}".format(size, "" if size == 1 else "s"))

            print()
            if size > 0:
                menu = "(A)dd  (E)dit  (L)ist  (R)emove  (Q)uit"
                valid = "aelrq"
            else:
                menu = "(A)dd  (Q)uit"
                valid = "aq"

            action = Console.get_menu_choice(
                menu,
                frozenset(valid),
                "l" if size else "a",
                True
            )

            functions[action](db)

def add_bookmark(db):
    name = Console.get_string("Name", "name")
    if not name:
        return

    if name in db and not Console.get_bool("Bookmark already exists, overwrite?", "no"):
        return

    url = Console.get_string("URL", "url")
    if not url:
        return

    db[name] = url
    db.sync()


def edit_bookmark(db):
    old_name = find_bookmark(db)
    if old_name is None:
        return

    name = Console.get_string("Name", "name", old_name)
    if not name:
        return

    url = Console.get_string("URL", "url", db[old_name])
    if not url:
        return

    db[name] = url
    if name != old_name:
        del db[old_name]
    db.sync()


def list_bookmarks(db):
    if len(db) > DISPLAY_LIMIT:
        start = Console.get_string("List bookmarks starting with "
                                   "[Enter=all]", "start")
    else:
        start = ""

    print()

    start = start.lower()
    index = 1

    for name in sorted(db, key=str.lower):
        if not start or name.lower().startswith(start):
            print("{:<4d} {:<20s} {}".format(index, name, db[name]))
            index += 1

    return start, index

def find_bookmark(db):
    start, max_index = list_bookmarks(db)
    index = Console.get_integer("Bookmark index", "bookmark", 0, 0, max_index)

    if index == 0:
        return None

    i = 1

    for name in sorted(db, key=str.lower):
        if not start or name.lower().startswith(start):
            if i == index:
                return name

            i += 1

def remove_bookmark(db):
    name = find_bookmark(db)
    if name is None:
        return

    ans = Console.get_bool("Remove {0}?".format(name), "no")
    if ans:
        del db[name]
        db.sync()

def quit_(db):
    size = len(db)
    print("Saved {0} bookmark{1}".format(size, "" if size == 1 else "s"))

    db.close()
    sys.exit()

if __name__ == '__main__':
    main()
