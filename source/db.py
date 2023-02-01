import sqlite3 as sql

def create_db():
    con=sql.connect("database.db")
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, user_id INTEGER, user_name TEXT, warning INTEGER)")
    con.commit()
    con.close()

def update_db(user_id, warning):
    con=sql.connect("database.db")
    cur=con.cursor()
    cur.execute("UPDATE users SET warning=? WHERE user_id=?", (warning, user_id))
    con.commit()
    con.close()

def view_db(user_id):
    con=sql.connect("database.db")
    cur=con.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    rows=cur.fetchall()
    con.close()
    return rows

def insert_db(user_id, user_name, warning):
    create_db()
    con=sql.connect("database.db")
    cur=con.cursor()
    user_data = view_db(user_id)
    if user_data:
        current_warning = user_data[0][-1]
        update_db(user_id, current_warning + warning)
    else:
        cur.execute("INSERT INTO users VALUES(NULL,?,?,?)", (user_id, user_name, warning))
    con.commit()
    con.close()

def delete_db(user_id):
    con=sql.connect("database.db")
    cur=con.cursor()
    cur.execute("DELETE FROM users WHERE user_id=?", (user_id,))
    con.commit()
    con.close()

def warn_user(user_id, user_name, warning):
    insert_db(user_id, user_name, warning)
    return view_db(user_id)[-1][-1]
