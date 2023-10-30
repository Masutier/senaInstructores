import os
import csv, json
import pandas as pd
import sqlite3 as sql3
from datetime import datetime, date
from flask import Flask, flash, render_template as render, redirect, request, jsonify
from dbsUtils import cursorExeAll

with open("/home/gabriel/prog/json_config/instructores.json") as config_file:
    sec_config = json.load(config_file)

app = Flask(__name__, static_url_path='/static')
app.secret_key = sec_config['SECRET_KEY']
now = datetime.now()

# Folder to aprendiz sqlite3
Sqlite_aprendiz_destiny_path = "../fichas_evaluacion_instructores/laprend/aprendiz.db"

# Folder to instructor sqlite3
Sqlite_instructor_destiny_path = "../fichas_evaluacion_instructores/linstr/instructor.db"

# Folder to testing instructors sqlite3
Sqlite_testing_destiny_path = "../fichas_evaluacion_instructores/testing.db"


@app.route('/', methods=['GET', 'POST'])
def home3():
    allApren = 0
    allInstr = 0
    allTest = 0

    # Buscar lista de aprendices
    sqlQuery1 = f"""SELECT * FROM aprendices"""
    aprend = cursorExeAll(Sqlite_aprendiz_destiny_path, sqlQuery1)

    # Buscar lista de Instructores
    sqlQuery2 = f"""SELECT * FROM instructores"""
    instruct = cursorExeAll(Sqlite_instructor_destiny_path, sqlQuery2)

    # Buscar todos los instructores calificados
    sqlQuery3 = f"""SELECT * FROM testing"""
    tested = cursorExeAll(Sqlite_testing_destiny_path, sqlQuery3)

    for i in aprend:
        allApren += 1
    print(allApren)

    for j in instruct:
        allInstr += 1
    print(allInstr)

    for k in tested:
        allTest += 1
    print(allTest)

    return render("home3.html", title="Instructores", allApren=allApren, allInstr=allInstr, allTest=allTest)



if __name__ == '__main__':
    #app.run(debug=True, host="172.16.170.60", port=8080)
    app.run(debug=True, host="localhost", port=5050)
