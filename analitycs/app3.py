import os
import csv, json
import pandas as pd
import sqlite3 as sql3
from datetime import datetime, date
from flask import Flask, flash, render_template as render, redirect, request, jsonify
from forms import *
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
    ficap = []
    ficin = []
    ficapqty = 0
    ficinqty = 0
    form = FichaForm()

    # Buscar lista de aprendices
    sqlQuery1 = f"""SELECT * FROM aprendices"""
    aprend = cursorExeAll(Sqlite_aprendiz_destiny_path, sqlQuery1)

    # Buscar lista de Instructores
    sqlQuery2 = f"""SELECT * FROM instructores"""
    instruct = cursorExeAll(Sqlite_instructor_destiny_path, sqlQuery2)

    for i in aprend:
        allApren += 1

    for j in instruct:
        allInstr += 1

    # Buscar fichas aprendices
    sqlQuery = f"""SELECT ficha FROM aprendices """
    conn1 = sql3.connect(Sqlite_aprendiz_destiny_path)
    cursor = conn1.cursor()
    fichasApr = cursor.execute(sqlQuery).fetchall()
    conn1.close()

    # Buscar fichas instructores
    sqlQuery = f"""SELECT fichas FROM instructores """
    conn2 = sql3.connect(Sqlite_instructor_destiny_path)
    cursor = conn2.cursor()
    fichasIns = cursor.execute(sqlQuery).fetchall()
    conn2.close()

    for fichaA in fichasApr:
        if fichaA not in ficap:
            ficap.append(fichaA)
            ficapqty += 1

    for fichaI in fichasIns:
        if fichaI not in ficin:
            ficin.append(fichaI)
            ficinqty += 1
    
    ficap.sort()
    ficin.sort()

    return render("home3.html", title="Analitycs", allApren=allApren, allInstr=allInstr, form=form, ficap=ficap, ficin=ficin, ficapqty=ficapqty, ficinqty=ficinqty)


@app.route('/ficha2', methods=['GET', 'POST'])
def ficha2():
    ficha2 = request.values.get('ficha')
    fichaAprendiz = []
    fichasInstructor = []


    # Buscar fichas aprendices
    sqlQuery = f"""SELECT * FROM aprendices WHERE FICHA = ? """
    conn1 = sql3.connect(Sqlite_aprendiz_destiny_path)
    cursor = conn1.cursor()
    fichasApr = cursor.execute(sqlQuery, (ficha2,)).fetchall()
    conn1.close()

    for aprend in fichasApr:
        if aprend not in fichaAprendiz:
            fichaAprendiz.append(aprend)

    # Buscar fichas instructores
    sqlQuery = f"""SELECT * FROM instructores WHERE FICHAS = ? """
    conn2 = sql3.connect(Sqlite_instructor_destiny_path)
    cursor = conn2.cursor()
    fichasInstructor = cursor.execute(sqlQuery, (ficha2,)).fetchall()
    conn2.close()

    return render("fichas2.html", title="fichas", ficha2=ficha2, fichaAprendiz=fichaAprendiz, fichasInstructor=fichasInstructor)


if __name__ == '__main__':
    #app.run(debug=True, host="172.16.170.60", port=8080)
    app.run(debug=True, host="localhost", port=5055)
