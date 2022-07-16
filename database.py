import sqlite3


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    __database_name = "manager.db"

    def __init__(self):
        self.database = sqlite3.connect(self.__database_name)
        self.cursor = self.database.cursor()

        if self._check_if_empty():
            self.create_new_data()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.database.close()

    def select(self, command):
        if command == "all":
            self.cursor.execute("SELECT * FROM paswords;")
            values = self.cursor.fetchall()
        else:
            self.cursor.execute("SELECT * FROM paswords WHERE site_name=:command;", {"command": command})
            values = self.cursor.fetchone()
        self.database.commit()
        return values


    def insert(self, email, password, login, site, stl):
        self.cursor.execute(
            """INSERT INTO paswords(email, pass, login, site_name, site_link)
                        VALUES(:email, :password, :login, :site, :stl);""",
            {
                "email": email,
                "password": password,
                "login": login,
                "site": site,
                "stl": stl
            }
        )
        self.database.commit()

    def update(self, column, old, new, site):
        if column == "site":
            column = "site_name"

        if site:
            self.cursor.execute("UPDATE paswords SET site_name=:new, site_link=:site WHERE site_name=:old;", {"new": new, "old": old, "site": site})
        else:
            self.cursor.execute(f"UPDATE paswords SET {column}=:new WHERE {column}=:old;", {"new": new, "old": old})
        self.database.commit()

    def delete(self, command):
        if command == "all":
            self.cursor.execute("DROP TABLE paswords;")
            self.create_new_data()
        else:
            self.cursor.execute("DELETE FROM paswords WHERE site_name=:command;", {"command": command})
        self.database.commit()

    def create_new_data(self):
        self.cursor.execute("""
            CREATE TABLE paswords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email text NOT NULL,
                pass character(16) NOT NULL,
                login text,
                site_name text NOT NULL,
                site_link text
            );""")
        self.database.commit()

    def _check_if_empty(self):
        self.cursor.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
        if not self.cursor.fetchall():
            return True
        else:
            return False
