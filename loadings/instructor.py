import os
import numpy as np
import pandas as pd
from datetime import datetime, date
from utils import semestre

# Directory for Aprentices
origen_path = "/home/gabriel/Downloads/fichas evaluacion instructores/instructores/"
# Folder to save csvs apprentice
instructor_destiny_path = "/home/gabriel/Downloads/fichas_evaluacion_instructores/linstr/"


# crear directorio si no existe
def crearInstructorFolder():
    newDir = semestre()
    try:
        os.makedirs(instructor_destiny_path + newDir)
        endDir = instructor_destiny_path + newDir
        return endDir
    except:
        endDir = instructor_destiny_path + newDir
        return endDir


def cleanSheets(sheet):
    # Clean Sheet names
    tbl_name = sheet.lower().replace(" ","_").replace("-","_").replace("$","").replace("?","").replace("%","") \
        .replace("Á","a").replace("É","e").replace("Í","i").replace("Ó","o").replace("Ú","u").replace("Ñ","n") \
        .replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n") \
        .replace("@","").replace("#","").replace(r"/","_").replace("\\","_").replace(r"(","").replace(")","")
    
    return tbl_name


    # Clean columns names
def cleanColNamesAll(dataframe, tbl_name):
    dataframe.columns = [x.lower().replace(" ","_").replace("-","_").replace("$","").replace("?","").replace("%","").replace(".","") \
        .replace("Á","a").replace("É","e").replace("Í","i").replace("Ó","o").replace("Ú","u").replace("Ñ","n") \
        .replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n") \
        .replace("@","").replace("#","").replace(r"/","").replace("\\","").replace(r"(","") \
        .replace(")","").replace(".","").replace("\n_anomesdia","").replace("\nanomesdia","") for x in dataframe.columns]
    
    # Create coordinacion table with the coordination name
    dataframe["coordinacion"] = tbl_name
    return dataframe.columns


    # Clean columns names
def cleanColNamesOne(dataframe, tbl_name):
    dataframe.columns = [x.lower().replace(" ","_").replace("-","_").replace("$","").replace("?","").replace("%","") \
        .replace("Á","a").replace("É","e").replace("Í","i").replace("Ó","o").replace("Ú","u").replace("Ñ","n") \
        .replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n") \
        .replace("@","").replace("#","").replace(r"/","").replace("\\","").replace(r"(","") \
        .replace(")","").replace(".","").replace("\n__anomesdia","").replace("\n__anomesdia","") for x in dataframe.columns]
    
    # Create coordinacion table with the coordination name
    dataframe["coordinacion"] = tbl_name
    return dataframe.columns


    # CLEAN DATA
def cleanData(dataframe):
    dataframe['no_identificacion_instructor'] = dataframe['no_identificacion_instructor'].astype(str)
    dataframe['no_identificacion_instructor'] = dataframe['no_identificacion_instructor'].fillna('NA')
    dataframe['ficha'] = dataframe['ficha'].ffill()
    dataframe['tipo_de_formacion'] = dataframe['tipo_de_formacion'].ffill()
    dataframe['programa_de_formacion'] = dataframe['programa_de_formacion'].ffill()
    dataframe['fecha_inicio_formacion'] = dataframe['fecha_inicio_formacion'].ffill()
    dataframe['fecha_finalizacion'] = dataframe['fecha_finalizacion'].ffill()
    dataframe['ficha'] = dataframe['ficha'].astype(str)
    dataframe['ficha'] = [x.replace(".0","") for x in dataframe['ficha']]

    return dataframe
    
