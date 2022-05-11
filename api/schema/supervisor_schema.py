import sqlite3

conn = sqlite3.connect("user.db")

cur = conn.cursor()

# cur.execute("DROP TABLE supervisor")

cur.execute("""CREATE TABLE IF NOT EXISTS supervisor (
                        id integer PRIMARY KEY,
                        email text NOT NULL UNIQUE,
                        fullname text NOT NULL,
                        user_id integer,
                        FOREIGN KEY (user_id)
                        REFERENCES user (user_id)
                            ON UPDATE RESTRICT
                            ON DELETE RESTRICT 
                        
                )""")

# print("Connection successful")


def insert_supervisor(id, email, fullname):
    with conn:
        cur.execute(
            "INSERT INTO supervisor (id, email, fullname) VALUES (?, ?, ?)",
            (id, email, fullname))


def get_supervisor(fullname):
    with conn:
        cur.execute("SELECT * FROM supervisor WHERE fullname = fullname")


def update_supervisor(id, email, fullname):
    with conn:
        cur.execute("""UPDATE supervisor SET
                                              id = id,
                                              email = email,
                                              fullname = fullname""")


def remove_supervisor(fullname):
    with conn:
        cur.execute("DELETE FROM supervisor WHERE fullname = fullname")


conn.commit()
conn.close()
