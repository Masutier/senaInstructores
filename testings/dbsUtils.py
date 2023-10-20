import sqlite3 as sql3


Sqlite_testing_destiny_path = "/home/gabriel/Downloads/fichas_evaluacion_instructores/testing.db"

conn = sql3.connect(Sqlite_testing_destiny_path)
cursor = conn.cursor()
cursor.execute('CREATE TABLE testing (ficha,aprendiz,instructor,p01,p02,p03,p04,p05,p06,p07,p08,p09,p10,p11,p12)')

conn.close()