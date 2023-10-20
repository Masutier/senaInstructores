import os
import csv, json
import pandas as pd
from datetime import datetime, date
from flask import Flask, flash, render_template as render, redirect, request, jsonify
import sqlite3 as sql3
from aprendiz import *
from instructor import *

with open("/home/gabriel/prog/json_config/instructores.json") as config_file:
    sec_config = json.load(config_file)

app = Flask(__name__, static_url_path='/static')
app.secret_key = sec_config['SECRET_KEY']
now = datetime.now()
year = now.strftime("%Y")

# Directory for xls
origen_path = "/home/gabriel/Downloads/fichas evaluacion instructores/aprendices/"
# Folder to aprendiz sqlite3
Sqlite_aprendiz_destiny_path = "/home/gabriel/Downloads/fichas_evaluacion_instructores/laprend/aprendiz.db"
# Folder to save csvs apprentice
Aprendice_destiny_path = "/home/gabriel/Downloads/fichas_evaluacion_instructores/laprend/"

# Folder to instructor sqlite3
Sqlite_instructor_destiny_path = "/home/gabriel/Downloads/fichas_evaluacion_instructores/linstr/instructor.db"
# Folder to save csvs instructor
instructor_destiny_path = "/home/gabriel/Downloads/fichas_evaluacion_instructores/linstr/"


def semestre():
    if now.strftime("%b") < "Jun":
        newDir = "I_SEM_" + year + "/"
    else:
        newDir = "II_SEM_" + year + "/"
    
    return newDir


@app.route('/', methods=['GET', 'POST'])
def home():

    return render("home.html", title="Home")


@app.route('/aprendiz', methods=['GET', 'POST'])
def aprendiz():
    sqlQuery = f"""
    
    SELECT * FROM aprendices"""

    conn = sql3.connect(Sqlite_aprendiz_destiny_path)
    cursor = conn.cursor()
    rows = cursor.execute(sqlQuery).fetchall()

    return render("aprendiz.html", title="Aprendices", rows=rows)


@app.route('/instructor', methods=['GET', 'POST'])
def instructor():
    sqlQuery = f"""SELECT * FROM instructores ORDER BY nombre_del_instructor ASC"""

    conn = sql3.connect(Sqlite_instructor_destiny_path)
    cursor = conn.cursor()
    rows = cursor.execute(sqlQuery).fetchall()

    return render("instructor.html", title="Instructores", rows=rows)


@app.route('/loadAprendices', methods=['GET', 'POST'])
def loadAprendices():
    frames=[]
    xls_files = []
    allApren = []

    # Create directory if not exists
    endDir = crearAprendizFolder()

    # Load only xls, xlsx files
    for file in os.listdir(origen_path):
        if file.endswith('.xls') or file.endswith('.xlsx'):
            ficha1 = []
            ficha = ""
            nnf = 6

            # Get ficha number
            data = pd.read_excel(io=origen_path + file, header=None)
            fechaReporte = data.iat[3,2]
            celx = data.iat[1,2]
            for i in celx:
                if nnf >= 0:
                    ficha1.append(i)
                    nnf -= 1
            ficha = ''.join(str(e) for e in ficha1)

            # Delete first 4 rows from file
            filenamex = file.split('.')
            dfx = pd.read_excel(io=origen_path + file, header=None)
            df1 = dfx.drop(dfx.index[0:4])
            df1.reset_index(drop=True, inplace=True)
            df1.drop(index=4)
            df1.columns = df1.iloc[0]
            df1 = df1[1:]

            # Add columns for fechaReporte and ficha
            df1['fecha_reporte'] = fechaReporte
            df1['ficha'] = ficha

            # Save processed sheets into one master dataframe
            allApren.append(df1)

            # Join all files in one dataframe
        dataframe = pd.concat(allApren, axis=0)
            # clean columns names and data
        dataframe = clean_colname(dataframe)
            # save to csv
        dataframe.to_csv(endDir + "allAprendices.csv", index=False)
        
            # DATABASE
        conn = sql3.connect(Sqlite_aprendiz_destiny_path)
        dataframe.to_sql(name="aprendices", con=conn, if_exists="append", index=False)
        conn.close()

        return redirect("aprendiz")


@app.route('/loadInstructores', methods=['GET', 'POST'])
def loadInstructores():
    allInstr = []
    if request.method == "POST":
            # crear directorio si no existe
        endDir = crearInstructorFolder()
            # Recibe xls file y separa nombre de la extension
        fileinn = request.files.get("fileinn")
        namefile = fileinn.filename
            # Extrae los nombres de las pestanas
        all_sheets = pd.read_excel(fileinn, sheet_name=None)
        sheets = all_sheets.keys()

        # Manipula cada csv
        for sheet in sheets:
            if sheet != 'LOGÍSTICA' and sheet != 'DATOS':
                dataframe = all_sheets[sheet]
                    # Limpia nombre de las pestanas
                tbl_name = cleanSheets(sheet)
                    # Limpia los titulos de columnas
                dataframe.columns = cleanColNamesAll(dataframe, tbl_name)
                    # Limpia la data
                dataframe = cleanData(dataframe)
                    # Save processed sheets into one master dataframe
                allInstr.append(dataframe)

            elif sheet == 'LOGÍSTICA':
                dataframe = all_sheets[sheet]
                    # Limpia nombre de las pestanas
                tbl_name = cleanSheets(sheet)
                    # Limpia los titulos de columnas
                dataframe.columns = cleanColNamesOne(dataframe, tbl_name)
                    # Limpia la data
                dataframe = cleanData(dataframe)
                    # Save processed sheets into one master dataframe
                allInstr.append(dataframe)

            # Join all files in one dataframe
        df = pd.concat(allInstr, axis=0)

            # save to csv
        df.to_csv(endDir + "allInstructores.csv", index=True)

        df = pd.read_csv(endDir + "allInstructores.csv")
        
            # DATABASE
        conn = sql3.connect(Sqlite_instructor_destiny_path)
        df.to_sql(name="instructores", con=conn, if_exists="append", index=False)
        conn.close()

    return redirect("instructor")


@app.route('/file404', methods=['GET', 'POST'])
def file404():

    return render("partials/file404.html", title="Error")


if __name__ == '__main__':
    #app.run(debug=True, host="172.16.170.128", port=8080)
    app.run(debug=True, host="localhost", port=5000)

