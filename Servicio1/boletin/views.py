from xml.dom import minidom
from django.shortcuts import render
from django.contrib.staticfiles.storage import staticfiles_storage
from flask import json
import requests
import webbrowser
import pdfkit
from .forms import RegForm, fForm, nitrForm, teForm, nitForm
import xml.etree.ElementTree as ET
from django.contrib import messages

pdf=[]

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
        print(http_response.text)
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
        print(http_response.text)
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
        'text': 'Para '+ str(NIT) +' como Emisor',
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
        pdf.append('<h2>Para el '+NIT+' como Emisor</h2>')
        pdf.append('<img src="'+strrr+'" alt="Grafica">') 
        
    context = {
        "el_form": form,
        "mostrar":mostrar,
        "grafica":strrr,
        "listaNIT":listaNIT,
        "NIT":NIT
    }
       
    
    return render(request,"resumen_iva.html",context)

def resumen_ivanr(request):
    mostrar=False
    form = nitrForm(request.POST or None)
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
        
        req = requests.Request('POST', 'http://192.168.1.9:3000/ObtenerNITR',headers=headers,data=xmlstr)
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
            nit_receptor = DTE.find('NIT_RECEPTOR').text.strip()
            NIT=nit_receptor
            
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
        'text': 'Para '+ str(NIT) +' como Receptor',
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
        pdf.append('<h2>Para el '+NIT+' como Receptor</h2>')
        pdf.append('<img src="'+strrr+'" alt="Grafica">') 
        
    context = {
        "el_form": form,
        "mostrar":mostrar,
        "grafica":strrr,
        "listaNIT":listaNIT,
        "NIT":NIT
    }    
       
    
    return render(request,"resumen_ivaNR.html",context)

def resumen_ivaf(request):
    mostrar=False
    form = fForm(request.POST or None)
    strrr=[]
    listaNIT=[]
    fecha=''
    NIT=''
    DatosGrafica=[]
    lis=[[],[],[],[],[]]
    if form.is_valid():
        mostrar=True
        form_data=form.cleaned_data
        nit=form_data.get("fecha")
        #con_iva=form_data.get("f")
        #print(con_iva)
        print(nit)
        a = ET.Element('SOLICITUD') 
        b = ET.SubElement(a, 'SELECCIONADO').text=str(nit)
        xmlstr = minidom.parseString(ET.tostring(a)).toprettyxml(indent="   ")

        headers = {'Content-Type': 'text/xml; charset=utf-8', }
        
        req = requests.Request('POST', 'http://192.168.1.9:3000/ObtenerFecha',headers=headers,data=xmlstr)
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
        val=[]
        horas=[]
        nits=[]
        primera=False
        for DTE in root.findall('TRANSACCION'):
            existe=True
            autorizacion = DTE.find('AUTORIZACION').text.strip()
            tiempo = DTE.find('TIEMPO').text.strip()
            referencia = DTE.find('REFERENCIA').text.strip()
            ref.append(referencia)
            nit_emisor = DTE.find('NIT_EMISOR').text.strip()
            nit_receptor = DTE.find('NIT_RECEPTOR').text.strip()
            NIT=nit_receptor
            fecha=tiempo.split(' ')[0]
            horas.append(tiempo.split(' ')[1])
            
            valor = DTE.find('VALOR').text.strip()
            val.append(float(valor))
            iva = DTE.find('IVA').text.strip()
            ie.append(float(iva))
            total = DTE.find('TOTAL').text.strip()
            ir.append(float(total))
            listaNIT.append([autorizacion,referencia,nit_emisor,nit_receptor,valor,iva,total])

            if DatosGrafica==[]:
                lis[0].append(nit_receptor)
                lis[1].append(valor)
                lis[2].append(iva)
                lis[3].append(total)
                lis[4].append(tiempo.split(' ')[1])
                DatosGrafica.append(lis)
                lis=[[],[],[],[],[]]
                

            if primera:
                for i in DatosGrafica:
                    if str(i[0][0]) == str(nit_receptor):
                        i[0].append(nit_receptor)
                        i[1].append(valor)
                        i[2].append(iva)
                        i[3].append(total)
                        i[4].append(tiempo.split(' ')[1])
                        existe=False
                if NIT not in nits:
                    lis[0].append(nit_receptor)
                    lis[1].append(valor)
                    lis[2].append(iva)
                    lis[3].append(total)
                    lis[4].append(str(tiempo.split(' ')[1]))
                    DatosGrafica.append(lis)
                    lis=[[],[],[],[],[]]
                    
            nits.append(NIT)
            primera=True

        print(DatosGrafica)
        for i in DatosGrafica:
            post_data = {'chart': {
            'type': 'line',
            'data': {
                'labels': i[4],
                'datasets': [
                {
                    'label': 'Precio',
                    'backgroundColor': 'rgb( 110, 255, 51)',
                    'borderColor': 'rgb( 110, 255, 51)',
                    'fill': 'false',
                    'data': i[1],
                },
                {
                    'label': 'IVA',
                    'backgroundColor': 'rgb(255, 99, 132)',
                    'borderColor': 'rgb(255, 99, 132)',
                    'fill': 'false',
                    'data': i[2],
                },
                {
                    'label': 'Total',
                    'backgroundColor': 'rgb(54, 162, 235)',
                    'borderColor': 'rgb(54, 162, 235)',
                    'fill': 'false',
                    'data': i[3],
                },
                ],
            },
            'options': {
            'title': {
            'display': 'true',
            'text': 'Moviemientos de '+ str(i[0][0]),
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
                strrr.append(chart_response['url'])

        messages.success(request,'')
        
        
    context = {
        "el_form": form,
        "mostrar":mostrar,
        "grafica":strrr,
        "listaNIT":listaNIT,
        "FECHA":fecha,
        "NIT": NIT,
    }   
    
    #pdfkit.from_url('http://127.0.0.1:8000/resumen_iva_fecha/','shaurya.pdf') 
    for i in strrr:
        pdf.append('<h2>En la fecha '+fecha+' el resumen del NIT '+NIT+' es:</h2>')
        pdf.append('<img src="'+i+'" alt="Grafica">')    
    
    return render(request,"resumen_ivaF.html",context)

def resumen_fechas(request):
    return 'hola'

def grafica(request):
    return 'hola'

def reporte_pdf(request):
    cadena=''
    for p in pdf:
        cadena+=p
    #pdf=[]
    pdfkit.from_string(cadena,'GfG.pdf')
    
    path = 'GfG.pdf'
    webbrowser.open_new(path)
    return render(request,"reporte_pdf.html")

