import os
import csv, json
import numpy as np
import pandas as pd
from datetime import datetime, date

with open("/home/gabriel/prog/json_config/instructores.json") as config_file:
    sec_config = json.load(config_file)

now = datetime.now()
year = now.strftime("%Y")


def semestre():
    if now.strftime("%b") < "Jun":
        newDir = "I_SEM_" + year + "/"
    else:
        newDir = "II_SEM_" + year + "/"
    
    return newDir


# Clean file name
def clean_tbl_name(csvf):
    CleanName = csvf.lower().replace(" ","_").replace("-","_").replace("$","").replace("?","").replace("%","") \
        .replace("Á","a").replace("É","e").replace("Í","i").replace("Ó","o").replace("Ú","u").replace("Ñ","n") \
        .replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n") \
        .replace("@","").replace("#","").replace(r"/","_").replace("\\","_").replace(r"(","").replace(")","")
    tbl_name = '{0}'.format(CleanName.split('.')[0])

    return tbl_name


# Create df with csv files
def csvFiles(endDir):
    csv_files = []
    for file in os.listdir(endDir):
        if file.endswith('.csv'):
            csv_files.append(file)
    df = {}
    for file in csv_files:
        try:
            df[file] = pd.read_csv(endDir + file)
        except:
            df[file] = pd.read_csv(endDir + file, encoding = "ISO-8859-1")

    return csv_files, df
