from xml.dom import minidom
from django.shortcuts import render
from django.contrib.staticfiles.storage import staticfiles_storage
from flask import json
import requests
from .forms import RegForm, fForm, nitrForm, teForm, nitForm
import xml.etree.ElementTree as ET
from django.contrib import messages


def inicio(request):
    return render(request,"inicio.html")

def cargar_archivo(request):
    form = RegForm(request.POST or None)
    form2 = teForm(request.POST or None)
    contenido=''
    if form.is_valid():
        form_data=form.cleaned_data
        ruta=form_data.get("ruta")
        with open(ruta,"r") as archivo:
            for linea in archivo:
                contenido+=str(linea)
        
        
        #root = ET.fromstring(contenido)
        headers = {'Content-Type': 'text/xml; charset=utf-8', }
        
        req = requests.Request('POST', 'http://192.168.1.9:3000/ObtenerDatos',headers=headers,data=contenido)
        prepped_requ = req.prepare()
        s = requests.Session()
        http_response = s.send(prepped_requ)
        #print(http_response.text)

        file = open('static/salida.xml', "w")
        file.write(str(http_response.text))
        file.close()
        messages.success(request,'Se agrego correctamente')

        print(staticfiles_storage.url('salida.xml'))
        
        
        #resp = requests.Request('POST','http://192.168.1.8:3000/ObtenerDatos',headers=headers,data=contenido)

    if form2.is_valid():
        form2_data=form2.cleaned_data
        contenido=str(form2_data.get("xml"))
        
        
        #root = ET.fromstring(contenido)
        headers = {'Content-Type': 'text/xml; charset=utf-8', }
        
        req = requests.Request('POST', 'http://192.168.1.9:3000/ObtenerDatos',headers=headers,data=contenido)
        prepped_requ = req.prepare()
        s = requests.Session()
        http_response = s.send(prepped_requ)
        #print(http_response.text)

        file = open('static/salida.xml', "w")
        file.write(str(http_response.text))
        file.close()
        messages.success(request,'Se agrego correctamente')

        print(staticfiles_storage.url('salida.xml'))

    context = {
        "el_form": form,
        "the_form": form2,
    }
    return render(request,"cargar_archivo.html",context)

def consulta_datos(request):
    return 'hola'

def resumen_iva(request):
    mostrar=False
    form = nitForm(request.POST or None)
    strrr=''
    listaNIT=[]
    NIT=''
    if form.is_valid():
        mostrar=True
        form_data=form.cleaned_data
        nit=form_data.get("nit")
        print(nit)
        a = ET.Element('SOLICITUD') 
        b = ET.SubElement(a, 'SELECCIONADO').text=str(nit)
        xmlstr = minidom.parseString(ET.tostring(a)).toprettyxml(indent="   ")

        headers = {'Content-Type': 'text/xml; charset=utf-8', }
        
        req = requests.Request('POST', 'http://192.168.1.9:3000/ObtenerNIT',headers=headers,data=xmlstr)
        prepped_requ = req.prepare()
        s = requests.Session()
        http_response = s.send(prepped_requ)
        #http_response.text
        quickchart_url = 'https://quickchart.io/chart/create'

        root = ET.fromstring(http_response.text)
        print(http_response.text)
        listaNIT=[]
        ir=[]
        ie=[]
        ref=[]
        for DTE in root.findall('TRANSACCION'):
            autorizacion = DTE.find('AUTORIZACION').text.strip()
            tiempo = DTE.find('TIEMPO').text.strip()
            referencia = DTE.find('REFERENCIA').text.strip()
            ref.append(referencia)
            nit_emisor = DTE.find('NIT_EMISOR').text.strip()
            NIT=nit_emisor 
            nit_receptor = DTE.find('NIT_RECEPTOR').text.strip()
            valor = DTE.find('VALOR').text.strip()
            iva = DTE.find('IVA').text.strip()
            ie.append(float(iva))
            total = DTE.find('TOTAL').text.strip()
            ir.append(float(total))
            listaNIT.append([autorizacion,tiempo, referencia,total,iva])

        post_data = {'chart': {
        'type': 'bar',
        'data': {
            'labels': ref,
            'datasets': [
            {
                'label': 'IVA Emitido',
                'backgroundColor': 'rgb(54, 162, 235)',
                'stack': 'Stack 1',
                'data': ir,
            },
            {
                'label': 'IVA Recibido',
                'backgroundColor': 'rgb(255, 99, 132)',
                'stack': 'Stack 2s',
                'data': ie,
            },
            
            ],
        },
        'options': {
        'title': {
        'display': 'true',
        'text': 'Bar Chart',
        },
        'plugins': {
        'datalabels': {
            'anchor': 'center',
            'align': 'center',
            'color': '#666',
            'font': {
            'weight': 'normal',
            },
        },
        },
    },
    },
}

        response = requests.post(
            quickchart_url,
            json=post_data
        )
        #print(listaNIT[0][0])

        if (response.status_code != 200):
            print('Error:', response.text)
        else:
            chart_response = json.loads(response.text)
            print(chart_response)
            strrr=chart_response['url']

        messages.success(request,'')
        
    context = {
        "el_form": form,
        "mostrar":mostrar,
        "grafica":strrr,
        "listaNIT":listaNIT,
        "NIT":NIT
    }    

    return render(request,"resumen_iva.html",context)

def resumen_fechas(request):
    return 'hola'

def grafica(request):
    return 'hola'

def reporte_pdf(request):
    return 'hola'

