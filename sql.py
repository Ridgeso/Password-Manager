"""
Scripts to manipulate the database
"""
import os
import sqlite3


def select(command):
    """
    Simple select command for extracting passwords
    """
    with sqlite3.connect("menager.bd") as passes:
        pa = passes.cursor()
        if command == "all":
            pa.execute("SELECT * FROM paswords")
            values = pa.fetchall()
        else:
            pa.execute("SELECT * FROM paswords WHERE site_name='{}'".format(command))
            values = pa.fetchone()
        passes.commit()
    return values


def insert(email, password, login, site, stl):
    """
    This function takes arguments from terminal.store_password function
    and database insertion
    """
    with sqlite3.connect("menager.bd") as passes:
        pa = passes.cursor()
        pa.execute(
            """INSERT INTO paswords VALUES (:email, :password, :login, :site, :stl)""",
            {
                "email": email,
                "password": password,
                "login": login,
                "site": site,
                "stl": stl
        })
        passes.commit()


def update(type_, old, new, site):
    """
    With terminal.update_password function here you can
    update values in databes
    """
    if type_ == "site":
        type_ = "site_name"
    with sqlite3.connect("menager.bd") as passes:
        pa = passes.cursor()
        if site:
            pa.execute(f"UPDATE paswords SET site_link='{site}' WHERE site_name='{old}'")
        pa.execute(f"UPDATE paswords SET {type_}='{new}' WHERE {type_}='{old}'")
        passes.commit()


def delete(command):
    """Deleting useless stuffs"""
    with sqlite3.connect("menager.bd") as passes:
        pa = passes.cursor()
        if command == "all":
            pa.execute("DELETE FROM paswords")
        else:
            pa.execute("DELETE FROM paswords WHERE site_name='{}'".format(command))
        passes.commit()


def create_new_data():
    """
    If the hole data base is broken here you can restart it
    """
    os.remove("menager.bd")
    with sqlite3.connect("menager.bd") as passes:
        pa = passes.cursor()
        pa.execute("""
            CREATE TABLE paswords (
                email text,
                pass text,
                login text,
                site_name text,
                site_link text
            )""")
        passes.commit()
