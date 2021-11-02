from django.http import HttpResponse
import datetime
from django.shortcuts import render
from django.template import loader

def inicio(request):
    doc=loader.get_template('index.html')
    documento=doc.render()
    return HttpResponse(documento)

def consulta_datos(request):
    doc=loader.get_template('consulta_datos.html')
    documento=doc.render()
    return HttpResponse(documento)

def cargar_archivo(request):
    doc=loader.get_template('cargar_archivo.html')
    documento=doc.render()
    return HttpResponse(documento)

def resumen_iva(request):
    doc=loader.get_template('resumen_iva.html')
    documento=doc.render()
    return HttpResponse(documento)

def resumen_fechas(request):
    doc=loader.get_template('resumen_fechas.html')
    documento=doc.render()
    return HttpResponse(documento)

def grafica(request):
    doc=loader.get_template('grafica.html')
    documento=doc.render()
    return HttpResponse(documento)

def reporte_pdf(request):
    doc=loader.get_template('reporte_pdf.html')
    documento=doc.render()
    return HttpResponse(documento)

def fecha(request):
    fecha_actual=datetime.datetime.now()
    
    fecha='''<html>
    <body>
    <h1>{% include "barra.html" %}
    Fecha y hora actuales {}
    {% include "pie.html" %}
    </h1>
    </body>
    </html>
    '''.format(fecha_actual)
    return HttpResponse(fecha)