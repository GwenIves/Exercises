#!/usr/bin/env python3
# Copyright (c) 2008-11 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version. It is provided for educational
# purposes and is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

import bisect
import contextlib
import copy
import gzip
import os
import pickle
import random
import socketserver
import struct
import sys
import threading

VERSION = 1


class Car:

    def __init__(self, seats, mileage, owner):
        self.__seats = seats
        self.mileage = mileage
        self.owner = owner


    @property
    def seats(self):
        return self.__seats


    @property
    def mileage(self):
        return self.__mileage


    @mileage.setter
    def mileage(self, mileage):
        self.__mileage = mileage


    @property
    def owner(self):
        return self.__owner


    @owner.setter
    def owner(self, owner):
        self.__owner = owner


class RequestHandler(socketserver.StreamRequestHandler):

    CarsLock = threading.Lock()

    def __init__(self, *args, **kwargs):
        self.Call = dict(
            GET_CAR_DETAILS=self.get_car_details,
            CHANGE_MILEAGE=self.change_mileage,
            CHANGE_OWNER=self.change_owner,
            NEW_REGISTRATION=self.new_registration,
            GET_LICENSES=self.get_licenses,
            SHUTDOWN=self.shutdown
        )

        super().__init__(*args, **kwargs)


    def handle(self):
        HeaderStruct = struct.Struct("!II")
        header_data = self.rfile.read(HeaderStruct.size)
        size, version = HeaderStruct.unpack(header_data)

        if version == VERSION:
            data = pickle.loads(self.rfile.read(size))

            function = self.Call[data[0]]
            reply = function(*data[1:])
        else:
            reply = False, "Unsupported client version %d" % (version, )

        data = pickle.dumps(reply, 3)
        self.wfile.write(HeaderStruct.pack(len(data), VERSION))
        self.wfile.write(data)

        if reply[0] is None:
            self.server.shutdown()


    def get_car_details(self, license):
        with RequestHandler.CarsLock:
            car = copy.copy(self.Cars.get(license, None))
        if car is not None:
            return (True, car.seats, car.mileage, car.owner)
        return (False, "This license is not registered")


    def get_licenses(self, prefix):
        with RequestHandler.CarsLock:
            licenses = list(self.Cars.keys())

        licenses.sort()
        result = []

        i = bisect.bisect_left(licenses, prefix)

        for l in licenses[i:]:
            if l.startswith(prefix):
                result.append(l)
            else:
                break

        return True, result

    def change_mileage(self, license, mileage):
        if mileage < 0:
            return (False, "Cannot set a negative mileage")
        with RequestHandler.CarsLock:
            car = self.Cars.get(license, None)
            if car is not None:
                if car.mileage < mileage:
                    car.mileage = mileage
                    return (True, None)
                return (False, "Cannot wind the odometer back")
        return (False, "This license is not registered")


    def change_owner(self, license, owner):
        if not owner:
            return (False, "Cannot set an empty owner")
        with RequestHandler.CarsLock:
            car = self.Cars.get(license, None)
            if car is not None:
                car.owner = owner
                return (True, None)
        return (False, "This license is not registered")


    def new_registration(self, license, seats, mileage, owner):
        if not license:
            return (False, "Cannot set an empty license")
        if seats not in {2, 4, 5, 6, 7, 8, 9}:
            return (False, "Cannot register car with invalid seats")
        if mileage < 0:
            return (False, "Cannot set a negative mileage")
        if not owner:
            return (False, "Cannot set an empty owner")
        with RequestHandler.CarsLock:
            if license not in self.Cars:
                self.Cars[license] = Car(seats, mileage, owner)
                return (True, None)
        return (False, "Cannot register duplicate license")


    @staticmethod
    def shutdown(*ignore):
        return None, "Server shutting down"


class CarRegistrationServer(socketserver.ThreadingMixIn,
                            socketserver.TCPServer): pass


def save(filename, cars):
    try:
        with contextlib.closing(gzip.open(filename, "wb")) as fh:
            pickle.dump(cars, fh, 3)
    except (EnvironmentError, pickle.UnpicklingError) as err:
        print("server failed to save data: {0}".format(err))
        sys.exit(1)


def load(filename):
    if not os.path.exists(filename):
        # Generate fake data
        cars = {}
        owners = []
        for forename, surname in zip(("Warisha", "Elysha", "Liona",
                "Kassandra", "Simone", "Halima", "Liona", "Zack",
                "Josiah", "Sam", "Braedon", "Eleni"),
                ("Chandler", "Drennan", "Stead", "Doole", "Reneau",
                 "Dent", "Sheckles", "Dent", "Reddihough", "Dodwell",
                 "Conner", "Abson")):
            owners.append(forename + " " + surname)
        for license in ("1H1890C", "FHV449", "ABK3035", "215 MZN",
                "6DQX521", "174-WWA", "999991", "DA 4020", "303 LNM",
                "BEQ 0549", "1A US923", "A37 4791", "393 TUT", "458 ARW",
                "024 HYR", "SKM 648", "1253 QA", "4EB S80", "BYC 6654",
                "SRK-423", "3DB 09J", "3C-5772F", "PYJ 996", "768-VHN",
                "262 2636", "WYZ-94L", "326-PKF", "EJB-3105", "XXN-5911",
                "HVP 283", "EKW 6345", "069 DSM", "GZB-6052", "HGD-498",
                "833-132", "1XG 831", "831-THB", "HMR-299", "A04 4HE",
                "ERG 827", "XVT-2416", "306-XXL", "530-NBE", "2-4JHJ"):
            mileage = random.randint(0, 100000)
            seats = random.choice((2, 4, 5, 6, 7))
            owner = random.choice(owners)
            cars[license] = Car(seats, mileage, owner)
        return cars
    try:
        with contextlib.closing(gzip.open(filename, "rb")) as fh:
            return pickle.load(fh)
    except (EnvironmentError, pickle.UnpicklingError) as err:
        print("server cannot load data: {0}".format(err))
        sys.exit(1)


def main():
    filename = os.path.join(os.path.dirname(__file__),
                            "car_registrations.dat")
    cars = load(filename)
    print("Loaded {0} car registrations".format(len(cars)))
    RequestHandler.Cars = cars
    server = None
    try:
        socketserver.ThreadingMixIn.allow_reuse_address = True
        server = CarRegistrationServer(("", 9653), RequestHandler)
        server.serve_forever()
    except Exception as err:
        print("ERROR", err)
    finally:
        if server is not None:
            server.shutdown()
            save(filename, cars)
            print("Saved {0} car registrations".format(len(cars)))


main()
