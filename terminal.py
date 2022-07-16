import database
import pyperclip
import security


class Terminal(database.Database):
    def __init__(self):
        self.hash = security.Hash()
        super(Terminal, self).__init__()

    def print_setup(self):
        print("\n###### Hello int your terminal setup ######")
        print("What do you want to do?")
        print("1. Get Pasword")
        print("2. Store Password")
        print("3. Delete Password")
        print("4. Update Database")
        print("5. Exit")

    def get_password(self):
        command = input("Type site related to this accounts: ")
        accounts = self.select(command)
        if not accounts:
            print("\nNo data found")
            return

        print()
        if command == "all":
            print("        email         |   passwords    |     login     |     site     |     site link")
            print("––––––––––––––––––––––+––––––––––––––––+–––––––––––––––+––––––––––––––+–––––––––––––––––––")
            for account in accounts:
                password = self.hash.inverse_cypher(account[2])
                print(f"{account[1]:<22}|{password:<16}|{account[3]:<15}|{account[4]:<14}|{account[5]:<13}")
                print("––––––––––––––––––––––+––––––––––––––––+–––––––––––––––+––––––––––––––+–––––––––––––––––––")
            print()
        else:
            print(f"email: {accounts[1]}")
            password = self.hash.inverse_cypher(accounts[2])
            pyperclip.copy(password)
            print(f"password: {password}\t has been copied to clipboard")
            if accounts[3]:
                print(f"login: {accounts[3]}")
            print(f"site: {accounts[4]}")
            if accounts[5]:
                print(f"site link: {accounts[5]}")
    
        input()


    def store_password(self):
        password = security.create_password()
        password = self.hash.cypher(password)

        email = input("Enter email: ")
        login = input("Enter login (not requried): ")
        site = input("Enter site: ")
        site_link = input("Enter site link (not requried): ")
        
        self.insert(email, password, login, site, site_link)

        print("\nDate has been added")


    def delete_password(self):
        command = input("Type site name of account you want to delete | None to leave: ")
        if not command:
            print("\nNo data has been deleted")
        else:
            self.delete(command)
            print("\nData has been deleted")


    def update_password(self):
        print("Column: email | login | site")
        column = input("What do you want to update: ")
        old = input(f"Enter current {column}: ")
        new = input(f"Enter new {column}: ")
        site = ""

        if column == "site":
            if input("Dou you want to update site link (y|n):").upper() in ("YES", "Y"):
                site = input("Enter new site link: ")
        
        self.update(column, old, new, site)

        print("\nData has been updeted")
