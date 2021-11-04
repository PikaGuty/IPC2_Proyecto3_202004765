from enum import auto
from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
from xml.dom import minidom

import re 
from datetime import datetime

#OBJETOS
from dte import Obj_DTE
from autorizado import Obj_aut

from validaciones import validaciones
from db import db


listaDB=[]
ret=[]

app = Flask(__name__)

@app.route('/ObtenerDatos',methods=['POST'])
def obtener_datos():
    xml_data = request.data
    xml=str(xml_data, 'utf-8')
    print(xml)
    root = ET.fromstring(xml)
    
    #****** SALIDA ******
    fecha=datetime.today().strftime('%d/%m/%Y')
    no_facturas=0
    errores=[]
    no_correctos=0
    no_emisores=0
    no_receptores=0
    aprob=[]
    #********************
    emi=[]
    rec=[]
    #****** SALIDA ******
    eFecha=0
    eReferencia=0
    ePrecio=0
    eIVA=0
    eTotal=0
    enite=0
    enitr=0
    eAut=0
    #********************

    for DTE in root.findall('DTE'):
        no_facturas+=1
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
            eFecha+=1
        elif res.valr == 'REFERENCIA_INVALIDA':
            print('Error en referencia')
            eReferencia+=1
        elif res.valp=='VALOR_INCORRECTO' or res.valp=='IVA_MAL_CALCULADO' or res.valp=='TOTAL_MAL_CALCULADO':
            print('Error en valores')
            if res.valp=='VALOR_INCORRECTO':
                ePrecio+=1
            elif res.valp=='IVA_MAL_CALCULADO':
                eIVA+=1
            elif res.valp=='TOTAL_MAL_CALCULADO':
                eTotal+=1
        elif not res.valne:
            print('Error en nite')
            enite+=1
        elif not res.valnr:
            print('Error en nitr')
            enitr+=1
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
                no_correctos+=1
                aprob.append([autorizacion,res.valf, referencia, nit_emisor, nit_receptor, valor, iva, total])
                listaDB.append([autorizacion,res.valf, referencia, nit_emisor, nit_receptor, valor, iva, total])
                db.insertar(listaDB)
                if nit_emisor in emi:
                    pass
                else:
                    no_emisores+=1

                if nit_receptor in rec:
                    pass
                else:
                    no_receptores+=1
            else:
                print('Error en numero de referencia')
                eAut+=1
    errores=[eFecha,eReferencia,ePrecio,eIVA,eTotal,enite,enitr,eAut]        
    ret=[fecha,no_facturas,errores,no_correctos,no_emisores,no_receptores,aprob]
    
    root = ET.Element("LISTAAUTORIZACIONES")
    doc = ET.SubElement(root, "AUTORIZACION")
    ET.SubElement(doc, "FECHA").text=str(fecha)
    ET.SubElement(doc, "FACTURAS_RECIBIDAS").text=str(no_facturas)
    EE=ET.SubElement(doc, "ERRORES")

    ET.SubElement(EE, "FECHAA").text=str(eFecha)
    ET.SubElement(EE, "REFERENCIA").text=str(eReferencia)
    ET.SubElement(EE, "PRECIO").text=str(ePrecio)
    ET.SubElement(EE, "IVA").text=str(eIVA)
    ET.SubElement(EE, "TOTAL").text=str(eTotal)
    ET.SubElement(EE, "NIT_EMISOR").text=str(enite)
    ET.SubElement(EE, "NIT_RECEPTOR").text=str(enitr)
    ET.SubElement(EE, "REFERENCIA_DUPLICADA").text=str(eAut)

    ET.SubElement(doc, "FACTURAS_CORRECTAS").text=str(no_correctos)
    ET.SubElement(doc, "CANTIDAD_EMISORES").text=str(no_emisores)
    ET.SubElement(doc, "CANTIDAD_RECEPTORES").text=str(no_receptores)
    LA=ET.SubElement(doc, "LISTADO_AUTORIZACIONES")
    for i in aprob:
        AP=ET.SubElement(LA, "APROBACION")
        ET.SubElement(AP, "NIT_EMISOR",ref=str(i[2])).text=str(i[3])
        ET.SubElement(AP, "CODIGO_APROBACION").text=str(i[0])
    ET.SubElement(LA, "TOTAL_APROBACIONES").text=str(no_correctos)
           
        
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")

    return str(xmlstr)

@app.route('/ReiniciarDatos',methods=['GET'])
def reiniciar_datos():
    db.reiniciar()
    return 'Datos eliminados'

@app.route('/ConsultaDatos',methods=['GET'])
def consulta_datos():
    
    return 'Consulta de Datos'

@app.route('/ConsultaNIT',methods=['GET'])
def consulta_NIT():
    listaDB=[]
    db.obtener(listaDB)
    #[autorizacion,tiempo, referencia, nit_emisor, nit_receptor, valor, iva, total]
    listadoNIT=[]
    for i in listaDB:
        if i[3] not in listadoNIT:
            listadoNIT.append(i[3])
    return str(listadoNIT)

@app.route('/ObtenerNIT',methods=['POST'])
def obtener_NIT():
    xml_data = request.data
    xml=str(xml_data, 'utf-8')
    print(xml)
    root = ET.fromstring(xml)
    selec = root.find('SELECCIONADO').text.strip()
    #print(selec)  
    listaDB=[]
    db.obtener(listaDB)
    #[autorizacion,tiempo, referencia, nit_emisor, nit_receptor, valor, iva, total]
    listadoNIT=[]
    for i in listaDB:
        if i[3] not in listadoNIT:
            listadoNIT.append(i[3])

    listaTransas=[]
    for i in listaDB:
        if listadoNIT[int(selec)]==i[3]:
            listaTransas.append(i)
#[autorizacion,tiempo, referencia, nit_emisor, nit_receptor, valor, iva, total]
    root = ET.Element("LISTAAUTORIZACIONES")
     
    for i in listaTransas:
        doc = ET.SubElement(root, "TRANSACCION")
        ET.SubElement(doc, "AUTORIZACION").text=str(i[0])
        ET.SubElement(doc, "TIEMPO").text=str(i[1])
        ET.SubElement(doc, "REFERENCIA").text=str(i[2])
        ET.SubElement(doc, "NIT_EMISOR").text=str(i[3])
        ET.SubElement(doc, "NIT_RECEPTOR").text=str(i[4])
        ET.SubElement(doc, "VALOR").text=str(i[5])
        ET.SubElement(doc, "IVA").text=str(i[6])
        ET.SubElement(doc, "TOTAL").text=str(i[7])
        
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")

    return str(xmlstr)



@app.route('/ConsultaNITR',methods=['GET'])
def consulta_NITR():
    listaDB=[]
    db.obtener(listaDB)
    #[autorizacion,tiempo, referencia, nit_emisor, nit_receptor, valor, iva, total]
    listadoNIT=[]
    for i in listaDB:
        if i[4] not in listadoNIT:
            listadoNIT.append(i[4])
    return str(listadoNIT)

@app.route('/ObtenerNITR',methods=['POST'])
def obtener_NITR():
    xml_data = request.data
    xml=str(xml_data, 'utf-8')
    print(xml)
    root = ET.fromstring(xml)
    selec = root.find('SELECCIONADO').text.strip()
    #print(selec)  
    listaDB=[]
    db.obtener(listaDB)
    #[autorizacion,tiempo, referencia, nit_emisor, nit_receptor, valor, iva, total]
    listadoNIT=[]
    for i in listaDB:
        if i[4] not in listadoNIT:
            listadoNIT.append(i[4])

    listaTransas=[]
    for i in listaDB:
        if listadoNIT[int(selec)]==i[4]:
            listaTransas.append(i)
#[autorizacion,tiempo, referencia, nit_emisor, nit_receptor, valor, iva, total]
    root = ET.Element("LISTAAUTORIZACIONES")
     
    for i in listaTransas:
        doc = ET.SubElement(root, "TRANSACCION")
        ET.SubElement(doc, "AUTORIZACION").text=str(i[0])
        ET.SubElement(doc, "TIEMPO").text=str(i[1])
        ET.SubElement(doc, "REFERENCIA").text=str(i[2])
        ET.SubElement(doc, "NIT_EMISOR").text=str(i[3])
        ET.SubElement(doc, "NIT_RECEPTOR").text=str(i[4])
        ET.SubElement(doc, "VALOR").text=str(i[5])
        ET.SubElement(doc, "IVA").text=str(i[6])
        ET.SubElement(doc, "TOTAL").text=str(i[7])
        
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")

    return str(xmlstr)

@app.route('/ConsultaFecha',methods=['GET'])
def consulta_Fecha():
    listaDB=[]
    db.obtener(listaDB)
    #[autorizacion,tiempo, referencia, nit_emisor, nit_receptor, valor, iva, total]
    listadoFecha=[]
    for i in listaDB:
        if str(i[1]).split(' ')[0] not in listadoFecha:
            listadoFecha.append(str(i[1]).split(' ')[0])
            #print(str(i[1].split(' ')[0]))
    return str(listadoFecha)

@app.route('/ObtenerFecha',methods=['POST'])
def obtener_Fecha():
    xml_data = request.data
    xml=str(xml_data, 'utf-8')
    print(xml)
    root = ET.fromstring(xml)
    selec = root.find('SELECCIONADO').text.strip()
    #print(selec)
    listaDB=[]
    db.obtener(listaDB)
    #[autorizacion,tiempo, referencia, nit_emisor, nit_receptor, valor, iva, total]
    listadoFecha=[]
    for i in listaDB:
        if str(i[1]).split(' ')[0] not in listadoFecha:
            listadoFecha.append(str(i[1]).split(' ')[0])
    
    listaTransas=[]
    for i in listaDB:
        if str(listadoFecha[int(selec)].split(' ')[0])==str(i[1]).split(' ')[0]:
            listaTransas.append(i)
#[autorizacion,tiempo, referencia, nit_emisor, nit_receptor, valor, iva, total]
    root = ET.Element("LISTAAUTORIZACIONES")
     
    for i in listaTransas:
        doc = ET.SubElement(root, "TRANSACCION")
        ET.SubElement(doc, "AUTORIZACION").text=str(i[0])
        ET.SubElement(doc, "TIEMPO").text=str(i[1])
        ET.SubElement(doc, "REFERENCIA").text=str(i[2])
        ET.SubElement(doc, "NIT_EMISOR").text=str(i[3])
        ET.SubElement(doc, "NIT_RECEPTOR").text=str(i[4])
        ET.SubElement(doc, "VALOR").text=str(i[5])
        ET.SubElement(doc, "IVA").text=str(i[6])
        ET.SubElement(doc, "TOTAL").text=str(i[7])
        
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")

    return str(xmlstr)

@app.route('/ResumenRango',methods=['POST'])
def resumen_rango():
    xml_data = request.data
    xml=str(xml_data, 'utf-8')
    print(xml)
    root = ET.fromstring(xml)
    f1 = root.find('FINICIO').text.strip()
    fe1 = f1.split('-')[2]+'/'+f1.split('-')[1]+'/'+f1.split('-')[0]
    fecha1 = datetime.strptime(fe1, '%d/%m/%Y')
    
    f2 = root.find('FFINAL').text.strip()
    fe2 = f2.split('-')[2]+'/'+f2.split('-')[1]+'/'+f2.split('-')[0]
    fecha2 = datetime.strptime(fe2, '%d/%m/%Y')

    listaDB=[]
    db.obtener(listaDB)
    #[autorizacion,tiempo, referencia, nit_emisor, nit_receptor, valor, iva, total]
    listaTransas=[]
    for i in listaDB:
        fechaA = datetime.strptime(str(i[1]).split(' ')[0], '%d/%m/%Y')
        if fecha1 <= fechaA <= fecha2:
            listaTransas.append(i)
    
    
    
    #[autorizacion,tiempo, referencia, nit_emisor, nit_receptor, valor, iva, total]
    root = ET.Element("LISTAAUTORIZACIONES")
     
    for i in listaTransas:
        doc = ET.SubElement(root, "TRANSACCION")
        ET.SubElement(doc, "AUTORIZACION").text=str(i[0])
        ET.SubElement(doc, "TIEMPO").text=str(i[1])
        ET.SubElement(doc, "REFERENCIA").text=str(i[2])
        ET.SubElement(doc, "NIT_EMISOR").text=str(i[3])
        ET.SubElement(doc, "NIT_RECEPTOR").text=str(i[4])
        ET.SubElement(doc, "VALOR").text=str(i[5])
        ET.SubElement(doc, "IVA").text=str(i[6])
        ET.SubElement(doc, "TOTAL").text=str(i[7])
        
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
    print(xmlstr)
    return str(xmlstr)

@app.route('/Grafica',methods=['GET'])
def grafica():
    return 'Grafica'

@app.route('/Procesar',methods=['POST'])
def procesar():
    return 'Procesar'

if __name__=="__main__":
    app.run(host="0.0.0.0",port=3000,debug=True)