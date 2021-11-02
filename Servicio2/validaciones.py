import re
from datetime import datetime

class validaciones():
    def __init__(self,tiempo, referencia, nit_emisor, nit_receptor, valor, iva, total):
        self.valf=self.fecha(tiempo)
        #print(self.valf)

        self.valr=self.referencia(referencia)
        #print(self.valr)

        self.valp=self.precios(valor,iva,total)
        #print(self.valp)

        self.valne=self.nit(nit_emisor)
        #print(self.valne)

        self.valnr=self.nit(nit_receptor)
        #print(self.valnr)


    def fecha(self,cadena):
        
        valido=True
        try:
            if re.search('[0-9]+/[0-9]+/[0-9]+',cadena) is not None:
                fecha=re.search('[0-9]+/[0-9]+/[0-9]+',cadena)
                try:
                    datetime.strptime(str(fecha.group()), '%d/%m/%Y')
                    fecha=fecha.group()
                except:
                    return 'FECHA INVALIDA'
        except:
            return 'FECHA INVALIDA'

        try:
            if re.search('[0-9]+:[0-9]+',cadena) is not None:
                hora=re.search('[0-9]+:[0-9]+',cadena)
                try:
                    datetime.strptime(str(hora.group()), '%H:%M')
                    hora=hora.group()
                except:
                    return 'HORA INVALIDA'
        except:
            return 'HORA INVALIDA'

        return str(fecha)+' '+str(hora)  

    def referencia(self,cadena):
        try:
            if len(cadena)<41:
                return cadena
            else:
                return 'REFERENCIA_INVALIDA'
        except:
            return 'REFERENCIA_INVALIDA'

    def precios(self,valor,iva,total):
        val=True
        valor=float(valor)
        iva=float(iva)
        total=float(total)
        
        try:
            if valor >0:
                valor=round(float(valor),2)
            else:
                return 'VALOR_INCORRECTO'
        except:
            return 'VALOR_INCORRECTO'

        try:
            if round(valor*0.12,2) == iva:
                pass
            else:
                return 'IVA_MAL_CALCULADO'
        except:
            return 'IVA_MAL_CALCULADO'

        try:
            if (valor+iva) == total:
                pass
            else:
                return 'TOTAL_MAL_CALCULADO'
        except:
            return 'TOTAL_MAL_CALCULADO'

        return [valor,iva,total]

    def nit(self,nit):
        try:
            if len(str(nit))>0 and len(str(nit))<22:
                u=str(nit)[len(str(nit))-1]
                nit=nit[:-1]
                numero = nit[::-1]
                suma=0
                contador=0
                mul=2
                for n in numero:
                    if mul !=7:
                        suma+=(int(n)*mul)
                        mul+=1
                    else:
                        suma+=(int(n)*mul)
                        mul=1
                
                mod1=suma%11
                val=11-mod1
                if val == 10:
                    val='K'
                if u.upper()==str(val):
                    return True
                else:
                    print(val)
                    return False
            else:
                return False
        except:
            return False
        