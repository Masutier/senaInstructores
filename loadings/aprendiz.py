import os
import numpy as np
import pandas as pd
from utils import semestre


# Directory for Aprentices
origen_path = "~/Downloads"
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


def clean_colname(dataframe):
    dataframe.columns = [x.lower().replace(" ","_").replace("-","_").replace("$","").replace("?","").replace("%","").replace(".","") \
        .replace("Á","a").replace("É","e").replace("Í","i").replace("Ó","o").replace("Ú","u").replace("Ñ","n") \
        .replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n") \
        .replace("@","").replace("#","").replace(r"/","").replace("\\","").replace(r"(","") \
        .replace(")","") for x in dataframe.columns]
    # CLEAN DATA
    dataframe['numero_de_documento'] = dataframe['numero_de_documento'].astype(str)
    dataframe['numero_de_documento'] = dataframe['numero_de_documento'].fillna('NA')
    dataframe['celular'] = dataframe['celular'].astype(str)
    dataframe['celular'] = dataframe['celular'].replace('nan', 'NA')
    dataframe['celular'] = dataframe['celular'].str.replace('.0', '')

    return dataframe
