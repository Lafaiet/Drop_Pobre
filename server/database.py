import sqlite3
from server_config import *


conn = sqlite3.connect(data_base)
cursor = conn.cursor()


def init_database():
    cursor.execute("""CREATE TABLE clients
                 (name text PRIMARY KEY,auth_key text,is_auth integer)
              """)

    cursor.execute("""CREATE TABLE dirs
                  (client text, dir text)
                   """)

def insert_client(client,h_key):
    sql="""INSERT INTO clients (name,auth_key,is_auth) VALUES (?,?,?)
        """
    cursor.execute(sql,(client,h_key,0))
    conn.commit()


def get_client(name):
    sql="""SELECT * FROM clients WHERE name=?
        """
    cursor.execute(sql,([name]))
    return cursor.fetchone()

def deauth_all():
    sql="select * from clients"
    cursor.execute(sql)
    cs=cursor.fetchall()

    for c in cs:
        sql="""
            UPDATE clients
            SET is_auth = 0
            WHERE name = ?
            """
        cursor.execute(sql,[c[0]])
        conn.commit()

def print_all():
    cursor.execute("select * from clients")
    print cursor.fetchall()  # ou use fetchone()


#init_database()
#insert_client("teste5", "chave")
#print_all()

