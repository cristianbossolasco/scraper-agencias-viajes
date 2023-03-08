from flask import Flask, jsonify, request, render_template, make_response, abort, redirect, url_for
import scraper_busplus_beautifulsoup as scraper
import pandas as pd 
from jinja2 import Template
import io
import base64
import xlsxwriter



app = Flask('API viajes')

# @app.route('/')
# def main():
#     return "Estoy disponible"




def dataframe_to_html_with_download(df, classes='', thead_classes=''):
    html_table = df.to_html(classes=classes)
    if thead_classes:
        html_table = html_table.replace('<thead>', '<thead class="{}">'.format(thead_classes))

    # Exporta el dataframe a un archivo de Excel en memoria
    excel_file = io.BytesIO()
    excel_writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    df.to_excel(excel_writer, sheet_name='Sheet1')
    excel_writer.save()
    excel_file.seek(0)

    # Convierte el archivo de Excel en una cadena base64
    excel_data = base64.b64encode(excel_file.read()).decode('utf-8')

    # Agrega un botón de descarga de Excel a la tabla
    download_button = '<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{}" download="data.xlsx">Descargar Excel</a>'.format(excel_data)
    html_table = html_table + '<div style="text-align: center; margin: auto;">{}</div>'.format(download_button)

    # Agrega el estilo CSS para centrar la tabla
    html_table = '<div style="text-align: center; margin: auto;">{}</div>'.format(html_table)
    html_table = html_table.replace('<table', '<table style="margin: auto;"')


    return html_table



@app.route('/getdata',methods=["GET"])
def get_data():
    
    ls_origenes = [28]
    df_paradas = scraper.get_paradas()
    ls_destinos = df_paradas.query('nombre.str.contains("Entre Rios")', engine='python').id.tolist()
    ls_destinos = df_paradas[6:7].id.tolist()

    result = scraper.scrapear_viajes(ls_origenes, ls_destinos, 1)
    df = scraper.dict_to_dataframe(result)
    
    classes = 'table table-striped table-bordered table-hover table-sm'
    thead_classes = "bg-primary text-white"
    html_table = dataframe_to_html_with_download(df, classes, thead_classes)
    return render_template("index.html", tabla=html_table)



@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/info',methods=["GET","POST"])
def inicio():
    cad=""
    cad+="<p>URL:"+request.url+"</p>\n"
    cad+="<p>Método:"+request.method+"</p>\n"

    cad+="<p>header:</p>\n"
    for item,value in request.headers.items():
        cad+="<p>{}:{}</p>\n".format(item,value)	

    cad+="<p>información en formularios (POST):</p>\n<ul>"
    for item,value in request.form.items():
        cad+="<li>{}:{}</li>\n".format(item,value)
    cad+="</ul>"
    
    cad+="<p>información en URL (GET):</p>\n<ul>"
    for item,value in request.args.items():
        cad+="<li>{}:{}</li>\n".format(item,value)    
    cad+="</ul>"

    cad+="<p>Ficheros:</p>\n<ul>"
    for item,value in request.files.items():
        cad+="<li>{}:{}</li>\n".format(item,value)
    cad+="</ul>"

    return cad



app.run(debug=True, port=8080)


