import database
import pyperclip
import security


class Terminal(database.Database):
    def __init__(self):
        self.hash = security.Hash()
        super(Terminal, self).__init__()

    def print_setup(self):
        print("###### Hello int your terminal setup ######")
        print("What do you want to do?")
        print("1. Get Pasword")
        print("2. Store Password")
        print("3. Delete Password")
        print("4. Update Database")
        print("5. Exit")

    def get_password(self):
        command = input("Type site related to this accounts: ")
        passwords = self.select(command)
        if passwords:
            if command == "all":
                print("        email         |     passwords      |     login     |     site     |     site link")
                print("––––––––––––––––––––––+––––––––––––––––––––+–––––––––––––––+––––––––––––––+–––––––––––––––––––")
                for data in passwords:
                    password = self.hash.encrypt(data[2])
                    print(f"{data[1]:<22}|{password:<20}|{data[3]:<15}|{data[4]:<14}|{data[5]:<13}")
                    print("––––––––––––––––––––––+––––––––––––––––––––+–––––––––––––––+––––––––––––––+–––––––––––––––––––")
                print()
            else:
                print(f"email: {passwords[1]}")
                password = self.hash.encrypt(passwords[1])
                pyperclip.copy(password)
                print(f"password: {password} has been copied to clipboard")
                if passwords[2]:
                    print(f"login: {passwords[3]}")
                print(f"site: {passwords[4]}")
                if passwords[4]:
                    print(f"site link: {passwords[5]}")
        else:
            print("No data found")


    def store_password(self):
        password = security.create_password()
        password = self.hash.decrypt(password)
        email = input("Enter email: ")
        login = input("Enter login (not requried): ")
        site = input("Enter site: ")
        site_link = input("Enter site link (not requried): ")
        self.insert(email, password, login, site, site_link)
        print("Date hasb been added")


    def delete_password(self):
        command = input("Type site name of account you want to delete | None to leave: ")
        if command == "None":
            print("No data has been deleted")
        else:
            self.delete(command)
            print("Data has been deleted")


    def update_password(self):
        print("Types: email | login | site")
        type_ = input("What do you want to update: ")
        old = input(f"Enter current {type_}: ")
        new = input(f"Enter new {type_}: ")
        site = ""
        if type_ == "site":
            if input("Dou you want to update site link (y|n):") in ("YES", "Y", "yes", "y"):
                site = input("Enter new site link: ")
        self.update(type_, old, new, site)
