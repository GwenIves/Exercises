#!/bin/env python3

import os
import struct
import tempfile

class BinaryRecordFile(object):
    def __init__(self, filename, record_size):
        self.__record_size = record_size

        if os.path.exists(filename):
            self.__fh = open(filename, "r+b")
            self.__size = self.__get_size()
        else:
            self.__fh = open(filename, "w+b")
            self.__size = 0

    def close(self):
        self.__fh.close()

    def append(self, record):
        self.__size += 1
        self[self.__size - 1] = record

    def __len__(self):
        return self.__size

    def __setitem__(self, index, record):
        if not isinstance(record, (bytes, bytearray)):
            raise ValueError("Invalid type to set: " + type(record))
        elif len(record) != self.__record_size:
            raise ValueError("Record to set must be exactly {} bytes long".format(
                self.__record_size))

        self.__seek_to_index(index)
        self.__fh.write(record)

    def __getitem__(self, index):
        self.__seek_to_index(index)

        return self.__fh.read(self.__record_size)

    def __delitem__(self, index):
        self.__seek_to_index(index)

        for i in range(index + 1, self.__size):
            self[index] = self[i]
            index += 1

        self.__size -= 1
        self.__fh.seek(self.__size * self.__record_size)
        self.__fh.truncate()

    def __seek_to_index(self, index):
        if index >= self.__size:
            raise IndexError("No record at index {}".format(index))

        self.__fh.seek(index * self.__record_size)

    def __get_size(self):
        self.__fh.seek(0, os.SEEK_END)

        return self.__fh.tell() // self.__record_size

class BikeStock(object):
    _BIKE_STRUCT = struct.Struct("<8s30sid")

    def __init__(self, identifier, name, quantity, price):
        if not identifier or not(3 <= len(identifier) <= 8):
            raise ValueError("Invalid identifier for a BikeStock: {}".format(identifier))

        self.__identifier = identifier
        self.name = name
        self.quantity = quantity
        self.price = price

    @property
    def size(self):
        return self._BIKE_STRUCT.size

    @property
    def identifier(self):
        return self.__identifier

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if not name or len(name) > 30:
            raise ValueError("BikeStock name must be between 1 and 30 characters long")

        self.__name = name

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, quantity):
        if(quantity < 0):
            raise ValueError("BikeStock quantity cannot be negative")

        self.__quantity = quantity

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        if(price <= 0.0):
            raise ValueError("BikeStock price must be positive")

        self.__price = price

    @property
    def value(self):
        return self.price * self.quantity

    def to_record(self):
        return BikeStock._BIKE_STRUCT.pack(
            self.identifier.encode("utf8"),
            self.name.encode("utf8"),
            self.quantity,
            self.price)

    @staticmethod
    def from_record(record):
        record = BikeStock._BIKE_STRUCT.unpack(record)

        return BikeStock(
            record[0].decode("utf8").rstrip("\x00"),
            record[1].decode("utf8").rstrip("\x00"),
            record[2],
            record[3])

    def __str__(self):
        return "{} @ {} of {}({})".format(self.quantity, self.price, self.identifier, self.name)


class BikeInventory(object):
    def __init__(self, filename):
        self.__file = BinaryRecordFile(filename, BikeStock.size)
        self.__id_to_index = {}

        for index in range(len(self.__file)):
            record = self.__file[index]
            stock = BikeStock.from_record(record)
            self.__id_to_index[stock.identifier] = index

    def close(self):
        self.__file.close()

    def add(self, stock):
        if stock.identifier in self.__id_to_index:
            raise ValueError("ID {} already present in inventory".format(stock.identifier))
        else:
            self.__id_to_index[stock.identifier] = len(self.__file)
            self.__file.append(stock.to_record())

    def __delitem__(self, identifier):
        removed_index = self.__id_to_index[identifier]

        del self.__file[removed_index]
        del self.__id_to_index[identifier]

        for identifier, index in self.__id_to_index.items():
            if index > removed_index:
                self.__id_to_index[identifier] -= 1

    def __getitem__(self, identifier):
        record = self.__file[self.__id_to_index[identifier]]
        return BikeStock.from_record(record)

    def __iter__(self):
        for index in range(len(self.__file)):
            yield BikeStock.from_record(self.__file[index])

    def change_stock(self, identifier, delta):
        index = self.__id_to_index[identifier]
        record = self.__file[index]
        stock = BikeStock.from_record(record)

        stock.quantity += delta
        self.__file[index] = stock.to_record()

def brf_test():
    print("BRF test")

    filename = os.path.join(tempfile.gettempdir(), "test1.dat")

    if os.path.exists(filename):
        os.remove(filename)

    f = BinaryRecordFile(filename, 10)

    S = struct.Struct("<10s")

    f.append(S.pack(b"Alpha"))
    f.append(S.pack(b"Beta"))
    f.append(S.pack(b"Gamma"))

    for i in range(len(f)):
        print(f[i])

    print()

    del f[1]
    f.append(S.pack(b"Omega"))

    for i in range(len(f)):
        print(f[i])

    print()

    f[1] = S.pack(b"Cyprus")

    for i in range(len(f)):
        print(f[i])

    f.close()

def inventory_test():
    print("\nInventory test")

    filename = os.path.join(tempfile.gettempdir(), "test2.dat")

    if os.path.exists(filename):
        os.remove(filename)

    bike_data = []
    bike_data.append(('REFK2', 'Reflex Kalahari', 5, 200.97))
    bike_data.append(('REFT1', 'Reflex Tempus', 4, 200.97))
    bike_data.append(('UNISTOW', 'Universal Stowaway', 1, 203.00))
    bike_data.append(('REFONA', "Reflex Out 'n' About", 0, 213.15))
    bike_data.append(('AMMC', 'Ammaco Commuter', 4, 259.84))

    bikes = BikeInventory(filename)

    for bike in bike_data:
        bikes.add(BikeStock(*bike))

    print(bikes["UNISTOW"])
    del bikes["UNISTOW"]

    bikes.change_stock("AMMC", 5)

    for stock in bikes:
        print(stock)

    bikes.close()

def main():
    brf_test()
    inventory_test()

if __name__ == '__main__':
    main()
