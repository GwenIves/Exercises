#!/bin/env python3

import os
import tempfile
import pickle

class ImageError(Exception): pass
class CoordinateError(ImageError): pass
class LoadError(ImageError): pass
class SaveError(ImageError): pass
class ExportError(ImageError): pass

class Image(object):
    RED = "#FF0000"
    GREEN = "#00FF00"
    BLUE = "#0000FF"
    WHITE = "#FFFFFF"
    BLACK = "#000000"

    def __init__(self, width, height, filename, background=WHITE):
        self.filename = filename
        self.__background = background
        self.__data = {}
        self.__width = width
        self.__height = height

    @property
    def background(self):
        return self.__background

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def colors(self):
        colors_set = set(self.__data.values())

        if len(self.__data) < self.width * self.height:
            colors_set |= {self.background}

        return colors_set

    def __check_coordinate(self, coordinate):
        if (len(coordinate) != 2 or
                not (0 <= coordinate[0] < self.width) or
                not (0 <= coordinate[1] < self.height)):
            raise CoordinateError(str(coordinate))

    def __getitem__(self, coordinate):
        self.__check_coordinate(coordinate)

        return self.__data.get(tuple(coordinate), self.__background)

    def __setitem__(self, coordinate, color):
        self.__check_coordinate(coordinate)

        if color == self.__background:
            self.__data.pop(tuple(coordinate), None)
        else:
            self.__data[tuple(coordinate)] = color

    def __delitem__(self, coordinate):
        self.__check_coordinate(coordinate)

        self.__data.pop(tuple(coordinate), None)

    def resize(self, width=None, height=None):
        shrink = False

        if width:
            if width < self.__width:
                shrink = True

            self.__width = width
        if height:
            if height < self.__height:
                shrink = True

            self.__height = height

        if shrink:
            new_data = {}

            for(x, y) in self.__data:
                if x <= self.__width and y <= self.__height:
                    new_data[(x, y)] = self.__data[(x, y)]

            self.__data = new_data

    def save(self):
        try:
            with open(self.filename, "wb") as fh:
                data = [self.width, self.height, self.__background, self.__data]
                pickle.dump(data, fh, pickle.HIGHEST_PROTOCOL)
        except(EnvironmentError, pickle.PicklingError) as err:
            raise SaveError(str(err))

    def load(self):
        try:
            with  open(self.filename, "rb") as fh:
                data = pickle.load(fh)
                (self.__width, self.__height, self.__background, self.__data) = data
        except(EnvironmentError, pickle.UnpicklingError) as err:
            raise LoadError(str(err))

    def export(self, filename):
        if filename.lower().endswith(".xpm"):
            self.__export_xpm(filename)
        else:
            raise ExportError("unsupported export format: " + os.path.splitext(filename)[1])

    @staticmethod
    def __get_xpm_chars(colors):
        RANGE_START = 32
        RANGE_STOP = 127
        RANGE_LEN = RANGE_STOP - RANGE_START - 2

        size = len(colors)

        if size <= RANGE_LEN:
            chars = [chr(x) for x in range(RANGE_START, RANGE_STOP) if chr(x) != '"']
        elif size <= RANGE_LEN * RANGE_LEN:
            chars = []

            for x in range(RANGE_START, RANGE_STOP):
                if chr(x) == '"':
                    continue

                for y in range(RANGE_START, RANGE_STOP):
                    if chr(y) == '"':
                        continue

                    chars.append(chr(x) + chr(y))
        else:
            raise ExportError("cannot export XPM: too many colors")

        chars.reverse()
        return chars

    def __export_xpm(self, filename):
        colors_set = self.colors()
        chars = self.__get_xpm_chars(colors_set)
        count = len(colors_set)

        fh = None
        try:
            name = os.path.splitext(os.path.basename(filename))[0]

            fh = open(filename, "w", encoding="ascii")
            fh.write("/* XPM */\n")
            fh.write("static char *{0}[] = {{\n".format(name))
            fh.write("/* columns rows colors chars-per-pixel */\n")
            fh.write('"{0.width} {0.height} {1} {2}",\n'.format(self, count, len(chars[0])))

            char_for_color = {}
            for color in colors_set:
                char = chars.pop()
                fh.write('"{char} c {color}",\n'.format(**locals()))
                char_for_color[color] = char

            fh.write("/* pixels */\n")

            for y in range(self.height):
                row = []

                for x in range(self.width):
                    color = self.__data.get((x, y), self.__background)
                    row.append(char_for_color[color])

                fh.write('"{0}",\n'.format("".join(row)))

            fh.write("};\n")
        except EnvironmentError as err:
            raise ExportError(str(err))
        finally:
            if fh is not None:
                fh.close()

def main():
    img_path = os.path.join(tempfile.gettempdir(), "test.img")
    xpm_path = os.path.join(tempfile.gettempdir(), "test.xpm")

    width, height = 240, 60
    mid_x, mid_y = width // 2, height // 2

    img = Image(width, height, img_path)

    for x in range(width):
        for y in range(height):
            if x < 5 or x >= width - 5 or y < 5 or y >= height - 5:
                img[x, y] = Image.RED
            elif mid_x - 20 < x < mid_x + 20 and mid_y - 20 < y < mid_y + 20:
                img[x, y] = Image.BLUE

    print(img.width, img.height, len(img.colors()), img.background)

    img.save()
    img.resize(width // 2, height)
    img.export(xpm_path)

    new_image = Image(1, 1, img_path)
    new_image.load()

    print(new_image.width, new_image.height, len(new_image.colors()), new_image.background)

if __name__ == '__main__':
    main()
