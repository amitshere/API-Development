from typing import Union

from fastapi import FastAPI
import sqlite3

app = FastAPI()

#Connect databse for records
def connect_to_db():
    conn = sqlite3.connect("record.db")
    c = conn.cursor()
    return (conn, c)

#get records as per query
def return_record(conn):
    record = []
    for row in conn:
        record.append(row)
    return record

#Create table
@app.get("/create_table")
def create_table():
    # Create a table
    conn, c = connect_to_db()
    c.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """
    )
    # Save (commit) the changes
    conn.commit()
    return f"Table record created in databse"


# insert data into table
@app.post("/insert_record")
def read_root(username: str, email: str):
    print(username)
    print(email)
    conn, c = connect_to_db()
    c.execute(
        f"""
    INSERT INTO users (username, email)
    VALUES ('{username}', '{email}')
    """
    )
    conn.commit()
    c.execute("SELECT * FROM users")
    return return_record(c)


# get data from the table
@app.get("/get_record")
def read_root():
    conn, c = connect_to_db()
    c.execute("SELECT * FROM users")
    return return_record(c)


# delete record and retrun remaning record
@app.delete("/delete_record")
def delete_record(username: str):
    conn, c = connect_to_db()
    c.execute(
        f"""
    DELETE FROM users
    WHERE username = '{username}'
    """
    )

    conn.commit()
    c.execute("SELECT * FROM users")
    conn.commit()
    return return_record(c)

#update table
@app.put("/update_record")
def update_record(username: str, email: str):
    conn, c = connect_to_db()
    c.execute(
        f"""
    UPDATE users
    SET email = '{email}'
    WHERE username = '{username}'
    """
    )
    c.execute("SELECT * FROM users")
    return return_record(c)
