from enum import auto
from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET

import re 
from datetime import datetime

#OBJETOS
from dte import Obj_DTE
from validaciones import validaciones
from db import db

listaDB=[]

app = Flask(__name__)

@app.route('/ObtenerDatos',methods=['POST'])
def obtener_datos():
    xml_data = request.data
    xml=str(xml_data, 'utf-8')
    print(xml)
    root = ET.fromstring(xml)
    for DTE in root.findall('DTE'):
        tiempo = DTE.find('TIEMPO').text.strip()
        referencia = DTE.find('REFERENCIA').text.strip()
        nit_emisor = DTE.find('NIT_EMISOR').text.replace(' ','')
        nit_receptor = DTE.find('NIT_RECEPTOR').text.replace(' ','')
        valor = DTE.find('VALOR').text.strip()
        iva = DTE.find('IVA').text.strip()
        total = DTE.find('TOTAL').text.strip()
        
        #print(tiempo, referencia, nit_emisor, nit_receptor, valor, iva, total)
        res=validaciones(tiempo, referencia, nit_emisor, nit_receptor, valor, iva, total)

        continuar=True
        
        if res.valf=='HORA INVALIDA'or res.valf=='FECHA INVALIDA':
            print('Error en fecha')
            continuar=False
        elif res.valr == 'REFERENCIA_INVALIDA':
            print('Error en referencia')
            continuar=False
        elif res.valp=='VALOR_INCORRECTO' or res.valp=='IVA_MAL_CALCULADO' or res.valp=='TOTAL_MAL_CALCULADO':
            print('Error en valores')
            continuar=False
        elif not res.valne:
            print('Error en nite')
            continuar=False
        elif not res.valnr:
            print('Error en nitr')
            continuar=False
        else:
            listaDB=[]
            db.obtener(listaDB)
            continuar=True
            fech=tiempo.split('/')
            dia=fech[0].split(' ')[1]
            mes=fech[1]
            ano=fech[2].split(' ')[0]
            fe=ano+mes+dia
            co=1
            for i in listaDB:
                if str(fe) != str(i[0][:-8]):
                    pass
                else:
                    co+=1
            ins=True
            for i in listaDB:
                if str(referencia) != str(i[2]):
                    pass
                else:
                    ins=False
            if ins:  
                correlativo='{num:08d}'.format(num=co)
                autorizacion=ano+mes+dia+correlativo
                listaDB.append([autorizacion,tiempo, referencia, nit_emisor, nit_receptor, valor, iva, total])
                db.insertar(listaDB)
            else:
                print('Error en numero de referencia')
            
    return str(type(xml))

@app.route('/ReiniciarDatos',methods=['GET'])
def reiniciar_datos():
    db.reiniciar()
    return 'Datos eliminados'

@app.route('/ConsultaDatos',methods=['GET'])
def consulta_datos():
    return 'Consulta de Datos'

@app.route('/ResumenIva',methods=['GET'])
def resumen_iva():
    return 'Resumen de Iva'

@app.route('/ResumenRango',methods=['GET'])
def resumen_rango():
    return 'Resumen Rango'

@app.route('/Grafica',methods=['GET'])
def grafica():
    return 'Grafica'

@app.route('/Procesar',methods=['POST'])
def procesar():
    return 'Procesar'

if __name__=="__main__":
    app.run(host="0.0.0.0",port=3000,debug=True)