# Write your code here
import random
import sqlite3
import sys


class User:
    acc_no = None
    pin = None
    balance = 0
    id = 0

    def luns(self, acc_num):
        count = 0
        sum = 0
        for digit in acc_num:
            digit = int(digit)
            count += 1
            if count % 2 == 1:
                digit = digit * 2
            if digit >= 10:
                digit -= 9
            sum += digit
        if sum % 10 == 0:
            return '0'
        else:
            check = str(10 - (sum % 10))
            return check

    def create_acc(self):
        acc_initial_num = '400000' + str(random.randrange(0, 9)) + str(random.randrange(0, 9)) + str(random.randrange(0, 9)) + str(random.randrange(0, 9)) + str(random.randrange(0, 9)) + str(random.randrange(0, 9)) + str(random.randrange(0, 9)) + str(random.randrange(0, 9)) + str(random.randrange(0, 9))
        self.acc_no = acc_initial_num + self.luns(acc_initial_num)
        self.pin = str(random.randrange(0, 9)) + str(random.randrange(0, 9)) + str(random.randrange(0, 9)) + str(random.randrange(0, 9))
        self.id += 1
        sql = "INSERT INTO card (id, number, pin, balance) VALUES (" + str(self.id) + ",'" + self.acc_no + "','" + self.pin + "'," + str(self.balance) + ");"
        conn.execute(sql)
        conn.commit()
        print()
        print("\nYour card has been created")
        print("Your card number:")
        print(self.acc_no)
        print("Your card PIN:")
        print(self.pin)
        return

    def transfer(self):
        print("\nTransfer")
        other_card = input("Enter card number:\n")
        last_digit = self.luns(other_card[:15])
        if last_digit != other_card[15]:
            print("Probably you made a mistake in the card number. Please try again!")
            self.after_login()
        else:
            if other_card == self.acc_no:
                print("You can't transfer money to the same account!")
                self.after_login()
            else:
                cur = conn.cursor()
                cur.execute("SELECT number FROM card WHERE number = ?", (other_card,))
                row = cur.fetchone()
                if row is None:
                    print("Such a card does not exist.")
                    self.after_login()
                else:
                    transfer_money = int(input("Enter how much money you want to transfer:\n"))
                    if self.balance < transfer_money:
                        print("Not enough money!")
                        self.after_login()
                    else:
                        self.balance -= transfer_money
                        cur.execute("UPDATE card SET balance = ? WHERE number = ?", (self.balance, self.acc_no))
                        cur.execute("SELECT balance FROM card WHERE number = ?", (other_card,))
                        row = cur.fetchone()
                        cur.execute("UPDATE card SET balance = ? WHERE number = ?", (row[0] + transfer_money, other_card))
                        conn.commit()
                        print("Success!")
                        self.after_login()

    def add_income(self):
        income = int(input("\nEnter income:\n"))
        if income < 0:
            self.after_login()
        else:
            self.balance += income
            conn.execute("UPDATE card SET balance = ? WHERE number = ?;", (self.balance, self.acc_no))
            conn.commit()
            print("Income was added!")
            self.after_login()

    def close_acc(self):
        conn.execute("DELETE FROM card WHERE number = ?;", (self.acc_no,))
        conn.commit()
        print("The account has been closed!")
        self.after_login()

    def after_login(self):
        while True:
            print()
            choice = int(input("\n1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n"))
            if choice == 1:
                print("\nBalance:", self.balance)
            elif choice == 2:
                self.add_income()
            elif choice == 3:
                self.transfer()
            elif choice == 4:
                self.close_acc()
            elif choice == 5:
                print()
                print("\nYou have successfully logged out!")
                self.main_menu()
            elif choice == 0:
                sys.exit()
            else:
                pass

    def log_acc(self):
        account_no = input("\nEnter your card number:\n")
        account_pin = input("Enter your PIN:\n")
        cur = conn.cursor()
        cur.execute("SELECT number, pin, balance FROM card WHERE number = ?;", (account_no,))
        row = cur.fetchone()
        if row is None:
            print()
            print("\nWrong card number or PIN!")
            self.main_menu()
        elif account_no != row[0] or account_pin != row[1]:
            print()
            print("\nWrong card number or PIN!")
            self.main_menu()
        else:
            self.acc_no = row[0]
            self.pin = row[1]
            self.balance = row[2]
            print()
            print("\nYou have successfully logged in!")
            self.after_login()

    def main_menu(self):
        while True:
            choice = int(input("\n1. Create an account\n2. Log into account\n0. Exit\n"))
            if choice == 1:
                user.create_acc()
            elif choice == 2:
                user.log_acc()
            elif choice == 0:
                sys.exit()
            else:
                pass


def create_db():
    conn.execute("DROP TABLE card")
    conn.execute("CREATE TABLE card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")
    conn.commit()


conn = sqlite3.connect('card.s3db')
user = User()
create_db()
user.main_menu()
