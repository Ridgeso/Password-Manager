"""
Welcome to my simple password menager, where you have
avaliable few functions to store, delete, update and finde
your passwords and logins from database
"""
from terminal import (
    get_password,
    store_password,
    delete_password,
    update_password,
    print_setup
)
import os


def main():
    while True:
        # os.system("clear")
        print_setup()
        command = input()

        if command == "1":
            get_password(input())
        elif command == "2":
            store_password()
        elif command == "3":
            delete_password(input())
        elif command == "4":
            update_password()
        elif command == "5":
            exit()
        # input()


if __name__ == '__main__':
    main()
