from functions import check_card

class Account:
    def __init__(self, con, cur, data):
        self.id = data.id
        self.card = data.card
        self.pin = data.pin
        self.balance = data.balance
        global connection, cursor
        connection = con
        cursor = cur

    def main_menu(self):
        options = ["1. Create an account", "2. Log into account", "0. Exit"]
        functions
    def account_menu(self):
        options = ["1. Balanace", "2. Log out", "0. Exit"]
        functions = {"1": self.balance, "2": self.log_out, "0": exit}
        print("", *options, sep="\n")
        choice = input(">").strip()
        if choice not in functions.keys():
            print("The option does not exist.\nPlease try again")
            return self.account_menu()
        else:
            functions[choice]()


    def balance(self):
        cursor.execute('select balance from card where number = ?', (self.card, ))
        self.balance = cursor.fetchone()[0]
        print('Balance: ', self.balance)
        return self.account_menu()

    def log_out(self):
        print("You have successfully logged out!")


