"""
Simple terminal file for terminal stuff xD
"""

import sql
import pyperclip
import hashes


def print_setup():
    print("###### Hello int your terminal setup ######")
    print("What do you want to do?")
    print("1. Get Pasword")
    print("2. Store Password")
    print("3. Dellete Password")
    print("4. Update Database")
    print("5. Exit")


def get_password(command):
    pa = sql.select(command)
    if pa:
        if command == "all":
            print("        email         |     passwords      |     login     |     site     |     site link")
            print("––––––––––––––––––––––+––––––––––––––––––––+–––––––––––––––+––––––––––––––+–––––––––––––––––––")
            for data in pa:
                password = hashes.encrypt(data[1])
                print(f"{data[0]:<22}|{password:<20}|{data[2]:<15}|{data[3]:<14}|{data[4]:<13}")
                print("––––––––––––––––––––––+––––––––––––––––––––+–––––––––––––––+––––––––––––––+–––––––––––––––––––")
            print()
        else:
            print(f"email: {pa[0]}")
            password = hashes.encrypt(pa[1])
            pyperclip.copy(password)
            print(f"password: {password} has been copied to clipboard")
            if pa[2]:
                print(f"login: {pa[2]}")
            print(f"site: {pa[3]}")
            if pa[4]:
                print(f"site link: {pa[4]}")
    else:
        print("No data found")


def store_password():
    password = hashes.create_password()
    password = hashes.decrypt(password)
    email = input("Enter email: ")
    login = input("Enter login (not requried): ")
    site = input("Enter site: ")
    site_link = input("Enter site link (not requried): ")
    sql.insert(email, password, login, site, site_link)
    print("Date hasb been added")


def delete_password(command):
    if command == "None":
        print("No data has been deleted")
    else:
        sql.delete(command)
        print("Data has been deleted")


def update_password():
    print("Types: email | login | site")
    type_ = input("What do you want to update: ")
    old = input(f"Enter current {type_}: ")
    new = input(f"Enter new {type_}: ")
    site = ""
    if type_ == "site":
        if input("Dou you want to update site link (y|n):") in ("YES", "Y", "yes", "y"):
            site = input("Enter new site link: ")
    sql.update(type_, old, new, site)
