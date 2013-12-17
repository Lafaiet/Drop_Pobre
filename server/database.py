import sqlite3
from server_config import *


conn = sqlite3.connect(data_base)
cursor = conn.cursor()


def init_database():
    cursor.execute("""CREATE TABLE clients
                 (name text PRIMARY KEY,auth_key text,salt text, is_auth integer)
              """)

    cursor.execute("""CREATE TABLE dirs
                  (client text, dir text)
                   """)

def insert_client(client,h_key,salt):
    sql="""INSERT INTO clients (name,auth_key,salt,is_auth) VALUES (?,?,?,?)
        """
    cursor.execute(sql,(client,h_key,salt,0))
    conn.commit()

def insert_dir(client,directory):
    sql="""INSERT INTO dirs (client,dir) VALUES (?,?)
        """
    cursor.execute(sql,(client,directory))
    conn.commit()

def get_client(name):
    sql="""SELECT * FROM clients WHERE name=?
        """
    cursor.execute(sql,([name]))
    return cursor.fetchone()

def get_clients_dir(directory):
    sql="""SELECT client FROM dirs WHERE dir=?
        """
    cursor.execute(sql,([directory]))
    r=[]
    for c in cursor.fetchall():
        r.append(c[0])

    return r

def get_dirs_client(client):
    sql="""SELECT dir FROM dirs WHERE client=?
        """
    cursor.execute(sql,([client]))
    return cursor.fetchall()

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


#print_all()
#print get_clients_dir("ful_dir")

