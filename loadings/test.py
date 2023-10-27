

@app.route('/loadAprendicesOne', methods=['GET', 'POST'])
def loadAprendicesOne():
    allAprendiz = []


    if request.method == "POST":
            # crear directorio si no existe
        endDir = crearInstructorFolder()


            # Recibe file y separa nombre de la extension
        fileinn = request.files.get("fileinn")
        filenamex = fileinn.split('.')

        if filenamex[1] == "csv":
            df = pd.read_csv(fileinn)
        if filenamex[1] == "xls":
            df = pd.read_excel(fileinn)
        if filenamex[1] == "xlsx":
            df = pd.read_excel(fileinn)

        print(df)




        # df = all_sheets[sheet]
        #     # Limpia nombre de las pestanas
        # tbl_name = cleanSheets(sheet)
        #     # Limpia los titulos de columnas
        # df.columns = cleanColNamesAll(df, tbl_name)
        #     # Limpia la data
        # df = cleanData(df)
        #     # Save processed sheets into one master df
        # allInstr.append(df)


    return redirect("aprendiz")