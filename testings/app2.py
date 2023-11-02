import os
import csv, json
import pandas as pd
import sqlite3 as sql3
from datetime import datetime, date
from flask import Flask, flash, render_template as render, redirect, url_for, request, jsonify
from forms import *
from dbsUtils import cursorExeOne, cursorExeAll

with open("/home/gabriel/prog/json_config/instructores.json") as config_file:
    sec_config = json.load(config_file)

app = Flask(__name__, static_url_path='/static')
app.secret_key = sec_config['SECRET_KEY']

# Folder to aprendiz sqlite3
Sqlite_aprendiz_destiny_path = "../fichas_evaluacion_instructores/laprend/aprendiz.db"
# Folder to save csvs apprentice
Aprendice_destiny_path = "../fichas_evaluacion_instructores/laprend/"

# Folder to instructor sqlite3
Sqlite_instructor_destiny_path = "../fichas_evaluacion_instructores/linstr/instructor.db"
# Folder to save csvs instructor
instructor_destiny_path = "../fichas_evaluacion_instructores/linstr/"

# Folder to testing instructors sqlite3
Sqlite_testing_destiny_path = "../fichas_evaluacion_instructores/testing.db"


@app.route('/', methods=['GET', 'POST'])
def home2():
    form = AprendizInfoForm()
    
    return render("home2.html", title="Instructores", form=form)


@app.route('/questionario', methods=['GET', 'POST'])
def questionario():
    aprendix = []
    ListaInstructores = []
    allInst = []
    instructoresFaltan = []

    # Datos del Aprendiz y numero de ficha
    ficha = request.form['ficha']
    name = request.form['name']
    lastname = request.form['lastname']
    document = request.form['tipoDoc']
    numdoc = request.form['numdoc']

    for i in request.form.values():
        aprendix.append(i)

    # Buscar el aprendiz en database para verificacion
    sqlQuery = f"""SELECT * FROM aprendices WHERE NUMERO_DOCUMENTO = ? """
    conn2 = sql3.connect(Sqlite_aprendiz_destiny_path)
    cursor = conn2.cursor()
    aprend = cursor.execute(sqlQuery, (numdoc,)).fetchone()
    conn2.close()

    if aprend:
        # Buscar lista de Instructores que dictan en la ficha
        sqlQuery = f"""SELECT * FROM instructores WHERE ficha = ? """
        conn2 = sql3.connect(Sqlite_instructor_destiny_path)
        cursor = conn2.cursor()
        instructores = cursor.execute(sqlQuery, (ficha,)).fetchall()
        conn2.close()

        if instructores:
            for instructor in instructores:
                if instructor not in ListaInstructores:
                    ListaInstructores.append(instructor)

            # Buscar si el instructor ya fue calificado por el aprendiz
            sqlQuery = f"""SELECT * FROM testing WHERE aprendiz = ? """
            conn2 = sql3.connect(Sqlite_testing_destiny_path)
            cursor = conn2.cursor()
            tested = cursor.execute(sqlQuery, (aprend[2],)).fetchall()
            conn2.close()

            for i in ListaInstructores:
                for j in tested:
                    if str(i[9]) == j[2]:
                        allInst.append(i)

            for l in ListaInstructores:
                if l not in allInst:
                    instructoresFaltan.append(l)
            
            form = AprendizEInstructor()
            
            return render("instructores.html", title="Instructores", instructoresFaltan=instructoresFaltan, aprendix=aprendix, form=form)
        else:
            flash("El numero de ficha no tiene asignados instructores o no es correcta")
            return redirect(url_for("home2"))
    else:
        flash("El numero de cedula no es correcto o no esta registrado")
        return redirect(url_for("home2"))


@app.route('/testing', methods=['GET', 'POST'])
def testing():
    instructorId = request.values.get('instructor')
    aprendizId = request.values.get('aprendiz')

    if instructorId:
        form = preguntasForm()

        # Buscar el aprendiz en database para verificacion
        sqlQuery = f"""SELECT * FROM aprendices WHERE NUMERO_DOCUMENTO = ? """
        conn2 = sql3.connect(Sqlite_aprendiz_destiny_path)
        cursor = conn2.cursor()
        aprendiz = cursor.execute(sqlQuery, (aprendizId,)).fetchone()
        conn2.close()

        # Buscar lista de Instructores que dictan en la ficha
        sqlQuery = f"""SELECT * FROM instructores WHERE no_identificacion_instructor = ? """
        conn2 = sql3.connect(Sqlite_instructor_destiny_path)
        cursor = conn2.cursor()
        instructor = cursor.execute(sqlQuery, (instructorId,)).fetchone()
        conn2.close()

        return render("questionario.html", title="Questionario", form=form, aprendiz=aprendiz, instructor=instructor)
    else:
        flash("Tienes que seleccionar un Instructor")
        return redirect(url_for("home2"))


@app.route('/saveTest', methods=['GET', 'POST'])
def saveTest():
    ficha = request.values.get('ficha')
    instructor = request.values.get('instructorid')
    aprendiz = request.values.get('aprendizid')
    p01 = request.values.get('p01')
    p02 = request.values.get('p02')
    p03 = request.values.get('p03')
    p04 = request.values.get('p04')
    p05 = request.values.get('p05')
    p06 = request.values.get('p06')
    p07 = request.values.get('p07')
    p08 = request.values.get('p08')
    p09 = request.values.get('p09')
    p10 = request.values.get('p10')
    p11 = request.values.get('p11')
    p12 = request.values.get('p12')

    if not p01 or not p05 or not p12:
        flash("Te faltaron algunas preguntas por responder, intentalo otra vez")
        return redirect(url_for("home2"))
    else:
        conn = sql3.connect(Sqlite_testing_destiny_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO testing (ficha,aprendiz,instructor,p01,p02,p03,p04,p05,p06,p07,p08,p09,p10,p11,p12) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (ficha,aprendiz,instructor,p01,p02,p03,p04,p05,p06,p07,p08,p09,p10,p11,p12))
        conn.commit()
        conn.close()

        flash("El cuestionario se gravo satisfactoriamente!")
        return redirect(url_for("home2"))


if __name__ == '__main__':
    #app.run(debug=True, host="172.16.170.60", port=8080)
    app.run(debug=True, host="localhost", port=5050)

