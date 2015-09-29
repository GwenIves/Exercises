#!/bin/env python3

import pickle
import os

class Transaction(Object):
	def __init__ (self, amount, date, ccy="USD", usd_conv_rate=1.0, desc=None):
		self.__amount = amount
		self.__date = date
		self.__ccy = ccy
		self.__usd_conv_rate = usd_conv_rate
		self.__desc = desc

	@property
	def amount (self):
		return self.__amount

	@property
	def date (self):
		return self.__date

	@property
	def ccy (self):
		return self.__ccy

	@property
	def usd_conv_rate (self):
		return self.__usd_conv_rate

	@property
	def desc (self):
		return self.__desc

	@property
	def usd (self):
		return self.amount * self.usd_conv_rate

class SavingError (Exception): pass
class LoadingError (Exception): pass

class Account(Object):
	def __init__ (self, acc_no, acc_name, transactions=list()):
		self.__acc_no = acc_no
		self.__transactions = transactions
		self.__set_name (acc_name)
		self.__all_usd = self.__check_all_usd ()
		self.__balance = self.__calculate_balance ()

	def __set_name (self, name):
		if len (name) < 4:
			raise ValueError ("Invalid value for the name attribute: " + name)
		else:
			self.__acc_name = name

	@property
	def acc_no (self):
		return self.__acc_no

	@property
	def all_usd (self):
		return self.__all_usd

	@property
	def balance (self):
		return self.__balance

	@property
	def acc_name (self):
		return self.__acc_name

	@acc_name.setter
	def acc_name (self, name):
		self.__set_name (name)

	def __len__ (self):
		return len (self.__transactions)

	def apply (self, transaction):
		if transaction.ccy != "USD":
			self.__all_usd = False

		self.__balance += transaction.usd
		self.__transactions.append (transaction)

	def save (self, directory):
		try:
			with open (self.__get_account_file (directory), "wb") as fh:
				data = [self.acc_name, self.__transactions]
				pickle.dump (data, fh, pickle.HIGHEST_PROTOCOL)
		except (EnvironmentError, pickle.PicklingError) as err:
			raise SavingError (str (err))

	def load (self, directory):
		try:
			with open (self.__get_account_file (directory), "rb") as fh:
				data = pickle.load (fh)

				self.__set_name (data[0])
				self.__transactions = data[1]
				self.__all_usd = self.__check_all_usd ()
				self.__balance = self.__calculate_balance ()
		except (EnvironmentError, IndexError, pickle.UnpicklingError) as err:
			raise LoadingError (str (err))

	def __get_account_file (self, directory):
		return os.path.join (directory, str (self.acc_no) + ".acc")

	def __check_all_usd (self):
		return all (map (lambda t: t.ccy == "USD", self.__transactions))

	def __calculate_balance (self):
		return sum (t.usd for t in self.__transactions)

def main ():
	a = Account (1, "Test_acc", [Transaction (100, "10-Oct-2014"), Transaction (20, "11-Oct-2014")])

	print (len (a))
	print (a.all_usd)
	print (a.balance)

	a.apply (Transaction (100, "12-Oct-2014", "EUR", 1.33))
	a.save ("/tmp")

	b = Account (1, "XXXX")
	b.load ("/tmp")

	print (len (b))
	print (b.all_usd)
	print (b.balance)

if __name__ == '__main__':
    main ()
