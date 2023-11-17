import os
import numpy as np
import pandas as pd
from datetime import datetime, date
from utils import semestre

# Folder to save csvs apprentice
instructor_destiny_path = "../fichas_evaluacion_instructores/linstr/"


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


    # Clean columns names
def clean_data_instructor(dataframe):
    dataframe.columns = [x.upper().replace(" ","_").replace("-","_").replace("$","").replace("?","").replace("%","").replace(".","") \
        .replace("Á","A").replace("É","E").replace("Í","I").replace("Ó","O").replace("Ú","U").replace("Ñ","N") \
        .replace("á","A").replace("é","E").replace("í","I").replace("ó","O").replace("ú","U").replace("ñ","N") \
        .replace("@","").replace("#","").replace(r"/","").replace("\\","").replace(r"(","") \
        .replace(")","").replace(".","").replace("\n_anomesdia","").replace("\nanomesdia","") for x in dataframe.columns]

    # CLEAN DATA

    dataframe['FICHA'] = dataframe['FICHA'].astype(str)
    dataframe['FICHA'] = [x.replace(".0","") for x in dataframe['FICHA']]

    dataframe['PROGRAMA_DE_FORMACION'] = dataframe['PROGRAMA_DE_FORMACION'].fillna('ND')

    dataframe['NUMERO_DE_DOCUMENTO'] = dataframe['NUMERO_DE_DOCUMENTO'].astype(str)
    dataframe['NUMERO_DE_DOCUMENTO'] = dataframe['NUMERO_DE_DOCUMENTO'].fillna('ND')

    return dataframe
    
