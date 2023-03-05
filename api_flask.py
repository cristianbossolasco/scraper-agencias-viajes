from flask import Flask, jsonify, request, render_template
import scraper_busplus_beautifulsoup as scraper
import pandas as pd 


app = Flask('API viajes')

@app.route('/')
def main():
    return "Estoy disponible"



@app.route('/getdata')
def get_data():
    
    ls_origenes = [28]
    df_paradas = scraper.get_paradas()
    ls_destinos = df_paradas.query('nombre.str.contains("Entre Rios")', engine='python').id.tolist()
    ls_destinos = df_paradas[5:8].id.tolist()

    result = scraper.scrapear_viajes(ls_origenes, ls_destinos, 1)
    # df_results = scraper.dict_to_dataframe(result)
    # ruta = '/content/drive/MyDrive/viajes/EntreRios_Next7_days.xlsx'
    # df_results.to_excel(ruta, index=False, encoding = 'utf-8-sig')
    return result


@app.route('/index')
def index():
    return render_template('index.html')


app.run(debug=True, port=8080)


