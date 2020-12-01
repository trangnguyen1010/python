import random
from collections import namedtuple
global connection, cursor
import sys
def luhn_algorithm(acc_number):
    acc_number = list(map(int, str(acc_number)))
    for i, _ in enumerate(acc_number, 1):
        if i % 2 != 0:
            acc_number[i-1] *= 2
        if acc_number[i-1] > 9:
            acc_number[i-1] -= 9
    return sum(acc_number)

def checksum(sum_number):
    return 10 - sum_number % 10 if sum_number % 10 != 0 else 0

def generate_account():
    account_number = 400000000000000 + random.randint(000000000, 999999999)
    luhn_num = luhn_algorithm(account_number)
    checksum_number = checksum(luhn_num)
    card_number = account_number*10 + checksum_number
    return card_number

def check_card(card_number):
    luhn_num = luhn_algorithm(card_number[:-1])
    check_sum = checksum(luhn_num)
    return check_sum == int(card_number[-1])

def generate_pin():
    pin = ""
    for _ in range(4):
        pin += str(random.randrange(10))
    return pin



def log_in_card_num() -> int:
    print()
    return int(input("Enter your card number:\n"))


def log_in_pass() -> int:
    print()
    return int(input("Enter your PIN:\n"))


def balance_input() -> int:
    print()
    return int(input("1. Balance\n2. Log out\n0. Exit\n"))


def balance():
    print()
    print("Balance: 0")


def log_out():
    print()
    print("You have successfully logged out!")


def compare(card_n, pin_n) -> int:
    global account
    global password
    if card_n == account:
        if pin_n == password:
            print("You have successfully logged in!")
            return 1
    else:
        return 0

def exit():
    print("Bye!")
    connection.close()
    sys.exit()

import sqlite3
from collections import namedtuple
conn = sqlite3.connect('card.s3db')
cursor = conn.cursor()
card_number = '4000000457698704'
Account = namedtuple('Account', 'id, card, pin, balance')
cursor.execute('select * from card')
list_card_balance = {}
for acc in map(Account._make, cursor.fetchall()):
        list_card_balance[acc.card] = acc.pin
balance = list_card_balance[card_number]
print("Balance: ", balance)
print(list_card_balance)