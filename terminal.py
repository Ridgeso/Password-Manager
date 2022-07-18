import database
import security


class Terminal(database.Database):
    KEY_LENGTH = 16
    def __init__(self) -> None:
        try:
            with open("key.bin", "rb") as secure:
                self.__key = secure.read(self.KEY_LENGTH)
        except FileNotFoundError:
            self.__key = self.generate_new_key(_init=True)
        
        if not self.__key:
            self.__key = self.generate_new_key(_init=True)
        
        super(Terminal, self).__init__()

    def generate_new_key(self, /, _init: bool=False) -> bytes:
        if not _init:
            decisiont = input("Are you sure you want to delete old key? [y/n]")
            if decisiont.upper() in ("NO", "N"):
                return
        
        with open("key.bin", "wb") as secure:
            new_key = security.create_password(self.KEY_LENGTH)
            secure.write(new_key.encode("ASCII"))
        return new_key

    def print_setup(self):
        print("""\n###### Hello int your terminal setup ######"""
            """\nWhat do you want to do?"""
            """\n1. Get Pasword"""
            """\n2. Store Password"""
            """\n3. Delete Password"""
            """\n4. Update Database"""
            """\n5. Exit""")
    
    def _print_all_accounts(self, accounts):
        encrypter = security.Hash(self.__key)
        print("""   |        email         |    passwords    |     login     |     site     |        URL"""
            """\n---––––-––––––––––––––––––+–-–––––––––––––––+–––––––––––––––+––––––––––––––+–––––––––––––––––––""")
        for i, account in enumerate(accounts, 1):
            password = encrypter.inverse_cypher(account.password)
            print(f"{i:<2} |{account.email:<22}|{password:<17}|{account.login:<15}|{account.site:<14}|{account.url:<13}")
            print("----––––––––––––––––––––––+-––––––––––––––––+–––––––––––––––+––––––––––––––+–––––––––––––––––––")

    def get_password(self):
        column = self._valid_column(("email", "login", "site", "all", ""))

        if not column:
            print("Skipped")
            return
        
        command = "" if column == "all" else input(f"Type {column} related to this accounts: ")
        accounts = self.select(column, command)
        if not accounts:
            print("\nNo data found")
            return
        print()

        if column == "all":
            self._print_all_accounts(accounts)
        else:
            account = self.multi_account_choice(accounts)

            account.password = security.Hash(self.__key).inverse_cypher(account.password)
            print(self._format_account(account))
            print("Password copied to clipboard")

        input("\nPress enter to continue")


    def store_password(self):
        password = security.create_password()
        encrypted_password = security.Hash(self.__key).cypher(password)

        email     = input("Email: ")
        login     = input("Login (not requried): ")
        site      = input("Site: ")
        url = input("Link to the website (not requried): ")
        print(f"Password: {password}")

        account = self.Account(email, encrypted_password, site, login, url)
        self.insert(account)

        input("\nData has been added, press enter to continue")


    def delete_password(self):
        column = self._valid_column(("email", "login", "site", "all", ""))
        if not column:
            print("Skipped")
            return
        
        if column == "all":
            self.drop_table()
            print("Database has been cleaned")
            return

        command = input(f'Type {column} related to this accounts: ')

        accounts = self.select(column, command)
        if not accounts:
            print("\nAccount not found")
            return
        else:
            account = self.multi_account_choice(accounts)

            self.delete(account)
            print("\nData has been deleted")

    def update_password(self):
        column = self._valid_column(("email", "login", "site", "url", ""))
        if not column:
            print("Skipped")
            return
        old_column = input(f"Enter current {column}: ")
        old = self.select(column, old_column)
        if not old:
            print("\nNo data found")
            return
        
        old = self.multi_account_choice(old)

        new_input = input(f"Enter new {column}: ")
        new = self.Account(old.email, old.password, old.site, old.login, old.url, old.id)
        setattr(new, column, new_input)

        if column == "site":
            if input("Dou you want to update website link [y/n]: ").upper() in ("YES", "Y"):
                url = input("Enter new website link: ")
                setattr(new, "url", url)
        
        self.update(old, new)
        print("\nData has been updeted")

    @staticmethod
    def _valid_column(fields):
        formated_fields = ' | '.join([field for field in fields if field])
        while (column := input(f"Search query [{formated_fields}]: ")) not in fields: pass
        return column