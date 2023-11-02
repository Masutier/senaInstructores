import os
import json

with open("/home/gabriel/prog/json_config/instructores.json") as config_file:
    sec_config = json.load(config_file)


# Folder to aprendiz sqlite3
Sqlite_aprendiz_destiny_path = "../fichas_evaluacion_instructores/laprend/aprendiz.db"

# Folder to instructor sqlite3
Sqlite_instructor_destiny_path = "../fichas_evaluacion_instructores/linstr/instructor.db"


# Create Aprendiz db
def createAprendizSqlite3():
    conn = sql3.connect(Sqlite_aprendiz_destiny_path)
    conn.commit()
    conn.close()


# Create instructor db
def createInstructorSqlite3():
    conn = sql3.connect(Sqlite_instructor_destiny_path)
    conn.commit()
    conn.close()

