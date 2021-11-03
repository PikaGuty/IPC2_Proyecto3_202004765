"""ejemplo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from boletin.views import inicio, cargar_archivo, consulta_datos, resumen_iva,resumen_fechas,grafica,reporte_pdf, resumen_ivaf, resumen_ivanr

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio, name='Inicio'),
    path('cargar_archivo/',cargar_archivo, name="CArchivo"),   
    path('consulta_datos/',consulta_datos, name="CDatos"),   
    path('resumen_iva_nitE/',resumen_iva, name="RIVA"),  
    path('resumen_iva_nitR/',resumen_ivanr, name="RIVANR"),  
    path('resumen_iva_fecha/',resumen_ivaf, name="RIVAF"),  
    path('resumen_fechas/',resumen_fechas, name="RFechas"),
    path('grafica/',grafica, name="Grafica"),   
    path('reporte_pdf/',reporte_pdf, name="RPDF"), 
]
