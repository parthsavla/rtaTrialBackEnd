import sqlite3

conn = sqlite3.connect("user.db")

cur = conn.cursor()

# cur.execute("DROP TABLE supervisor")
cur.execute("""CREATE TABLE IF NOT EXISTS notification (
                        id integer PRIMARY KEY,
                        title text NOT NULL UNIQUE,
                        date_posted text NOT NULL,
                        content text,
                        supervisor_name text NOT NULL,
                        supervisor_email text NOT NULL,
                        major text NOT NULL,
                        education text NOT NULL,
                        user_id integer,
                        FOREIGN KEY (user_id)
                        REFERENCES user (user_id)
                            ON UPDATE RESTRICT
                            ON DELETE RESTRICT 
                        
                )""")

# print("Connection successful")


def insert_notification(id, title, date_posted, content, supervisor_name,
                        supervisor_email, major, education):
    with conn:
        cur.execute(
            "INSERT INTO notification (id, title, date_posted, content, supervisor_name, supervisor_email, major, education) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (id, title, date_posted, content, supervisor_name,
             supervisor_email, major, education))


def get_notification(user_id):
    with conn:
        cur.execute("SELECT * FROM notification WHERE user_id = user_id")


def update_notification(id, title, date_posted, content, supervisor_name,
                        supervisor_email, major, education):
    with conn:
        cur.execute("""UPDATE notification SET
                                              id, title, date_posted, content, supervisor_name,supervisor_email, major, education"""
                    )


def remove_notification(user_id):
    with conn:
        cur.execute("DELETE FROM notification WHERE user_id = user_id")


conn.commit()
conn.close()
