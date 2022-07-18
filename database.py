import sqlite3
import pyperclip


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    __database_name = "manager.db"

    class Account:
        __slots__ = "id", "email", "password", "login", "site", "url"
        def __init__(self, email, password, site, login="", url="", id=-1) -> None:
            self.id = id
            self.email = email
            self.password = password
            self.login = login
            self.site = site
            self.url = url

        @classmethod
        def _array_to_account(cls, arr):
            return cls(arr[1], arr[2], arr[4], arr[3], arr[5], arr[0])
        
        def __repr__(self) -> str:
            return f"Account(email: {self.email}, website: {self.site}, login: {self.login or None})"

    def __init__(self) -> None:
        self.database = sqlite3.connect(self.__database_name)
        self.cursor = self.database.cursor()

        if self._check_if_database_empty():
            self._create_new_data()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.database.close()

    def commit_action(self) -> None:
        self.database.commit()

    def select(self, column: str, command: str) -> list[Account]:
        if column == "all":
            self.cursor.execute("SELECT * FROM paswords;")
        else:
            self.cursor.execute(f"SELECT * FROM paswords WHERE {column}=:command;", {"command": command})

        values = self.cursor.fetchall()
        self.database.commit()
        return [self.Account._array_to_account(val) for val in values]

    def insert(self, account: Account) -> None:
        self.cursor.execute(
            """INSERT INTO paswords(email, pass, login, site, url)
                        VALUES(:email, :password, :login, :site, :stl);""",
            {
                "email": account.email,
                "password": account.password,
                "login": account.login,
                "site": account.site,
                "stl": account.url
            })
        self.commit_action()

    def drop_table(self) -> None:
        if input("Sure want to delete all databes? [y/n]").upper() in ("YES", "Y"):
            self.cursor.execute("DROP TABLE paswords;")
            self._create_new_data()
        
    def delete(self, account: Account) -> None:
        self.cursor.execute(f"DELETE FROM paswords WHERE email=:email AND login=:login AND site=:site;",{
            "email": account.email,
            "login": account.login,
            "site": account.site
        })
        self.commit_action()

    def update(self, old: Account, new: Account) -> None:
        self.cursor.execute("""UPDATE paswords
                            SET email=:n_email, login=:n_login, site=:n_site, url=:n_url
                            WHERE email=:o_email AND login=:o_login AND site=:o_site AND url=:o_url;""",
            {
                "n_email": new.email, "n_login": new.login, "n_site": new.site, "n_url": new.url,
                "o_email": old.email, "o_login": old.login, "o_site": old.site, "o_url": old.url
            })
        self.commit_action()

    def multi_account_choice(self, accounts: list[Account]) -> Account:
        if len(accounts) == 1:
            return accounts[0]
        
        print(self._repr_accounts(accounts))

        while account_pos := input(f"Choose which 1-{len(accounts)} (enter to continue): "):
            if not account_pos.isdigit():
                continue

            account_pos = int(account_pos) - 1
            if 0 > account_pos >= len(account_pos):
                continue
            
            break
        return accounts[account_pos]

    def _create_new_data(self) -> None:
        self.cursor.execute("""
            CREATE TABLE paswords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email text NOT NULL,
                pass character(16) NOT NULL,
                login text,
                site text NOT NULL,
                url text
            );""")
        self.commit_action()    

    def _format_account(self, account: Account) -> str:
        pyperclip.copy(account.password)

        format_string = f"email:     {account.email}\npassword:  {account.password}"
        if account.login:
            format_string += f"\nlogin:     {account.login}"
        format_string += f"\nsite:      {account.site}"
        if account.url:
            format_string += f"\nsite link: {account.url}"
        
        return format_string

    def _check_if_database_empty(self) -> bool:
        self.cursor.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
        if not self.cursor.fetchall():
            return True
        else:
            return False
    
    def _repr_accounts(self, accounts: list[Account]) -> str:
        formated_accounts = ""
        for i, account in enumerate(accounts, 1):
            formated_accounts += f"{i:<2} - {account}\n"
        return formated_accounts
