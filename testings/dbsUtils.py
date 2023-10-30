import sqlite3 as sql3


def cursorExeOne(address, sqlQuery, data):
    conn2 = sql3.connect(address)
    cursor = conn2.cursor()
    databack = cursor.execute(sqlQuery, (data,)).fetchone()
    conn2.close()

    return databack


def cursorExeAll(address, sqlQuery, data):
    conn2 = sql3.connect(address)
    cursor = conn2.cursor()
    databack = cursor.execute(sqlQuery, (data,)).fetchall()
    conn2.close()

    return databack

