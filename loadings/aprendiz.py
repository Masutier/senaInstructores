import os
import numpy as np
import pandas as pd
from datetime import datetime, date
from utils import semestre

# Folder to save csvs apprentice
Aprendice_destiny_path = "../fichas_evaluacion_instructores/laprend/"


# crear directorio si no existe
def crearAprendizFolder():
    newDir = semestre()
    try:
        os.makedirs(Aprendice_destiny_path + newDir)
        endDir = Aprendice_destiny_path + newDir
        return endDir
    except:
        if os.listdir(Aprendice_destiny_path + newDir):
            endDir = Aprendice_destiny_path + newDir
            return endDir


def clean_data_aprendiz(dataframe):
    dataframe.columns = [x.upper().replace(" ","_").replace("-","_").replace("$","").replace("?","").replace("%","").replace(".","") \
        .replace("Á","A").replace("É","E").replace("Í","I").replace("Ó","O").replace("Ú","U").replace("Ñ","N") \
        .replace("á","A").replace("é","E").replace("í","I").replace("ó","O").replace("ú","U").replace("ñ","N") \
        .replace("@","").replace("#","").replace(r"/","").replace("\\","").replace(r"(","") \
        .replace(")","") for x in dataframe.columns]

    # CLEAN DATA
    dataframe['FICHA'] = dataframe['FICHA'].astype(str)
    dataframe['FICHA'] = [x.replace(".0","") for x in dataframe['FICHA']]

    dataframe['NUMERO_DE_DOCUMENTO'] = dataframe['NUMERO_DE_DOCUMENTO'].astype(str)
    dataframe['NUMERO_DE_DOCUMENTO'] = dataframe['NUMERO_DE_DOCUMENTO'].fillna('ND')

    dataframe['CELULAR'] = dataframe['CELULAR'].astype(str)
    dataframe['CELULAR'] = dataframe['CELULAR'].replace('nan', 'ND')
    dataframe['CELULAR'] = dataframe['CELULAR'].str.replace('.0', '')

    dataframe['CORREO_ELECTRONICO'] = dataframe['CORREO_ELECTRONICO'].fillna('ND')

    dataframe['ESTADO'] = dataframe['ESTADO'].fillna('ND')

    return dataframe
