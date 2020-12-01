import sqlite3
from functions import generate_account, generate_pin, check_card
from collections import namedtuple
import sys

class Banking:
    # create account for handling SQL query
    Account = namedtuple('Account', 'id, card, pin, balance')
    # init() function:
    def __init__(self):
        global cursor, connection
        connection = sqlite3.connect('card.s3db')
        cursor = connection.cursor()
        connection.row_factory = sqlite3.Row
        cursor.execute('CREATE TABLE if not exists card ('+
                        'id integer Primary Key,'+
                        'number TEXT not null,'+
                        'pin TEXT not null, balance Integer Default 0' +
                       ')')
        connection.commit()
        # show main menu
        self.main_menu()

    def main_menu(self):
        option =["1. Create an account", "2. Log into account", "0. Exit"]
        functions = {"1": self.create_account, "2": self.log_in, "0": self.exit}
        print("", *option, sep="\n")
        choice = input(">").strip()
        if choice not in functions.keys():
            print("This option does not exit.\nPlease try again")
        else:
            functions[choice]()
        return self.main_menu()


    # Function login to account:
    def log_in(self):
        print("Enter your card number:")
        card_number = input(">").strip()
        print("Enter your PIN:")
        pin = input(">").strip()
        account = self.get_account(card_number, pin)
        if account:
            print("You have successfully logged in!")
            self.account_menu()
            while True:
                choice = self.select_account_option()
                if choice == "1":
                    self.balance(card_number)
                elif choice == "2":
                    self.add_income(card_number)
                elif choice == "3":
                    self.do_transfer(card_number)
                elif choice == "4":
                    self.close_account(card_number)
                elif choice == "5":
                    self.log_out()
                    return self.main_menu()
                elif choice == "0":
                    self.exit()
            #account.account_menu()

        else:
            print("Wrong card number or PIN!")

    def create_account(self):
        print("Your card has been created")
        accounts = self.get_all_accounts()
        while True:
            card_number = generate_account()
            if card_number not in accounts.keys():
                break
        pin = generate_pin()
        print("Your card number:", card_number, "Your card PIN:", pin, sep="\n")
        cursor.execute('insert into card(number, pin) values(?, ?)', (card_number, pin))
        connection.commit()


    def get_all_accounts(self):
        accounts = {}
        cursor.execute('select * ' +
                       'from card')
        for acc in map(self.Account._make, cursor.fetchall()):
            accounts[acc.card] = acc.pin
        return accounts


    def get_account(self, account_number, pin):
        cursor.execute("select *" +
                        "from card " +
                        "where number = ? and pin = ?", (account_number, pin))
        f = cursor.fetchone()
        return self.Account._make(f) if f else None

    def account_menu(self):
        options = ["1. Balance", "2. Add income", "3. Do transfer", "4. Close account", "5. Log out", "0. Exit"]
        print("", *options, sep="\n")

    def select_account_option(self):
        choice = input(">").strip()
        return choice

    def balance(self, card_number):
        balance = self.get_balance(card_number)
        print("Balance: ", balance)
        return self.account_menu()

    def get_balance(self, card_number):
        cursor.execute('select * from card where number = ?', (card_number,))
        list_card_balance = {}
        for acc in map(self.Account._make, cursor.fetchall()):
            list_card_balance[acc.card] = acc.balance
        balance = list_card_balance[card_number]
        return balance


    def add_income(self, card_number):
        print("Enter income:")
        income = input(">").strip()
        current_balance = self.get_balance(card_number)
        new_balance = int(income) + current_balance
        cursor.execute('update card set balance = ? where number = ?', (new_balance, card_number))
        connection.commit()
        print("Income was added!")
        return self.account_menu()

    def do_transfer(self, card_transfer):
        print("Transfer")
        print("Enter card number:")
        card_number = input(">").strip()
        check_account = self.validate_card_transfer(card_number)
        if check_account:
            print("Enter how much money you want to transfer:")
            money_transfer = input(">").strip()
            balance = self.get_balance(card_transfer)
            if int(money_transfer) > balance:
                print("Not enough money")
                self.account_menu()
            else:
                print("Success!")
                new_balance = balance - int(money_transfer)
                cursor.execute('update card set balance = ? where number = ?', (new_balance, card_transfer))
                connection.commit()
                cursor.execute('update card set balance = ? where number = ?', (money_transfer, card_number))
                connection.commit()
                self.account_menu()
        elif not check_card(card_number):
            print("Probably you made a mistake in the card number. Please try again!")
            self.account_menu()
        else:
            print("Such a card does not exist.")
            self.account_menu()


    def validate_card_transfer(self, card_number):
        cursor.execute("select * from card where number = ?", (card_number,))
        f = cursor.fetchone()
        return self.Account._make(f) if f else None

    def close_account(self, card_number):
        print("The account has been closed!")
        cursor.execute('delete from card where number = ?', (card_number, ))
        connection.commit()
        return self.main_menu()

    def log_out(self):
        print("YOu have successfully logged out!")

    def exit(self):
        print("Bye!")
        connection.close()
        sys.exit()



def main():
    bank = Banking()

if __name__ == '__main__':
    main()
