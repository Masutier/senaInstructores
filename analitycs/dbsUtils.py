import sqlite3 as sql3


def cursorExeAll(address, sqlQuery):
    conn2 = sql3.connect(address)
    cursor = conn2.cursor()
    databack = cursor.execute(sqlQuery).fetchall()
    conn2.close()

    return databack

