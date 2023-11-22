import os
import csv, json
import pandas as pd
import sqlite3 as sql3
from openpyxl import Workbook, load_workbook
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

# Folder to testing instructors sqlite3
Excel_report_destiny_path = "../fichas_evaluacion_instructores/"


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
    sqlQuery = f"""SELECT FICHA FROM aprendices """
    conn1 = sql3.connect(Sqlite_aprendiz_destiny_path)
    cursor = conn1.cursor()
    fichasApr = cursor.execute(sqlQuery).fetchall()
    conn1.close()

    # Buscar fichas instructores
    sqlQuery = f"""SELECT FICHA FROM instructores """
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
    sqlQuery = f"""SELECT * FROM instructores WHERE FICHA = ? """
    conn2 = sql3.connect(Sqlite_instructor_destiny_path)
    cursor = conn2.cursor()
    fichasInstructor = cursor.execute(sqlQuery, (ficha2,)).fetchall()
    conn2.close()

    return render("fichas2.html", title="fichas", ficha2=ficha2, fichaAprendiz=fichaAprendiz, fichasInstructor=fichasInstructor)


@app.route('/retriveFichas', methods=['GET', 'POST'])
def retriveFichas():
    testings = []
    notestings = []
    dataToReport = []

    with open("../fichas_evaluacion_instructores/fichas.json") as fichas:
        fichas = json.load(fichas)

    for ficha in fichas:
        fichax = str(ficha)

        # Buscar lista de Instructores que dictan en la ficha
        sqlQuery = f"""SELECT * FROM testing WHERE FICHA = ? """
        conn1 = sql3.connect(Sqlite_testing_destiny_path)
        cursor = conn1.cursor()
        fichaA = cursor.execute(sqlQuery, (fichax,)).fetchone()
        conn1.close()

        if fichaA:
            apreId = fichaA[1]
            instId = fichaA[2]

            # Buscar Aprendiz que califico
            sqlQuery = f"""SELECT * FROM aprendices WHERE NUMERO_DE_DOCUMENTO = ? """
            conn1 = sql3.connect(Sqlite_aprendiz_destiny_path)
            cursor = conn1.cursor()
            aprendiz = cursor.execute(sqlQuery, (apreId,)).fetchone()
            conn1.close()

            # Buscar Instructor calificado
            sqlQuery = f"""SELECT * FROM instructores WHERE NUMERO_DE_DOCUMENTO = ? """
            conn2 = sql3.connect(Sqlite_instructor_destiny_path)
            cursor = conn2.cursor()
            instructor = cursor.execute(sqlQuery, (instId,)).fetchone()
            conn2.close()
        
            x = 3
            xxx = 0
            divisor = 1
            for item in range(11):
                x += 1
                if fichaA[x] != None:
                    y = int(fichaA[x])
                    xxx += y
                    divisor += 1

            resp = xxx/divisor
            items = [fichaA, aprendiz, instructor, resp]
            testings.append(items)

            record = [fichaA[0], aprendiz[2], aprendiz[3], aprendiz[4], instructor[3], instructor[4], instructor[5], str(round(resp, 2))]
            dataToReport.append(record)

        else:
            notestings.append(fichax)

        # save to excel
    FilePath = Excel_report_destiny_path + "reporte_evaluacion_instructores.xlsx"

        # Creating first dataframe
    data1 = pd.DataFrame(data=dataToReport, columns=['FICHA', 'NUM_DOC_APRENDIZ', 'NOMBRE_APRENDIZ', 'APELLIDO_APRENDIZ', 'NUM_DOC_INSTRUCTOR', 'NOMBRE_INSTRUCTOR', 'APELLIDO_INSTRUCTOR', 'CALIFICACION_PROMEDIO'])

        # Creating second dataframe
    data2 = pd.DataFrame(data=notestings, columns=['FICHA'])

        # Adding the DataFrames to the excel as a new sheets
    with pd.ExcelWriter(FilePath) as writer:
        data1.to_excel(writer, sheet_name='Promedios', index=False)
        data2.to_excel(writer, sheet_name='No Participaron', index=False)

    return render("tests.html", title="Analitycs", testings=testings, notestings=notestings)


if __name__ == '__main__':
    #app.run(debug=True, host="172.16.170.60", port=8080)
    app.run(debug=True, host="localhost", port=5055)
