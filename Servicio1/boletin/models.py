from django.db import models
import requests

class Registrados(models.Model):
    nombre = models.CharField(max_length=100,blank=True,null=True)
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)

    def __unicode__(self):
        return self.email

    def __str__(self):
        return self.email


class NITE(models.Model):
    r =requests.get('http://192.168.1.9:3000/ConsultaNIT')
    l=r.text.split('[')[1].split(']')[0]
    lista=l.split(',')
    tup=[]
    c=0
    for i in lista:
        st=(c,i.split('\'')[1])
        c+=1
        tup.append(st)
    nit=models.IntegerField(null=False, blank=False, choices=tup)

class NITR(models.Model):
    r =requests.get('http://192.168.1.9:3000/ConsultaNITR')
    l=r.text.split('[')[1].split(']')[0]
    lista=l.split(',')
    tup=[]
    c=0
    for i in lista:
        st=(c,i.split('\'')[1])
        c+=1
        tup.append(st)
    nit=models.IntegerField(null=False, blank=False, choices=tup)

class FECHA(models.Model):
    r =requests.get('http://192.168.1.9:3000/ConsultaFecha')
    l=r.text.split('[')[1].split(']')[0]
    lista=l.split(',')
    tup=[]
    c=0
    for i in lista:
        st=(c,i.split('\'')[1])
        c+=1
        tup.append(st)
    nit=models.IntegerField(null=False, blank=False, choices=tup)

