import sqlite3

conn = sqlite3.connect("user.db")

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS user (
                        id integer PRIMARY KEY,
                        email text NOT NULL UNIQUE,
                        fname text NOT NULL,
                        lname text NOT NULL,
                        regdate text NOT NULL,
                        admin integer NOT NULL,
                        user_id integer NOT NULL UNIQUE,
                        username text NOT NULL UNIQUE,
                        department text NOT NULL,
                        passwordhash text NOT NULL UNIQUE
                )""")
# print("Connection successful")


def insert_user(id, email, fname, lname, regdate, admin, user_id, username,
                department, passwordhash):
    with conn:
        cur.execute(
            "INSERT INTO user (id, email, fname, lname, regdate, admin, user_id, username, department, passwordhash) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (id, email, fname, lname, regdate, admin, user_id, username,
             department, passwordhash))


def get_user(fname, lname):
    with conn:
        cur.execute("SELECT * FROM user WHERE fname = fname AND lname = lname")


def update_user(id, email, fname, lname, regdate, admin, user_id, username,
                department, passwordhash):
    with conn:
        cur.execute("""UPDATE user SET
                                              id = id,
                                              email = email,
                                              fname = fname,
                                              lname = lname,
                                              regdate = regdate,
                                              admin = admin,
                                              user_id = user_id,
                                              username = username,
                                              department = department,
                                              passwordhash = passwordhash""")


def remove_user(fname, lname):
    with conn:
        cur.execute("DELETE FROM user WHERE fname = fname and lname = lname", )


conn.commit()
conn.close()
