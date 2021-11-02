class Obj_aut():
    def __init__(self,Autorizacion,Fecha,Referencia,Nit_Emisor,Nit_Receptor,Valor,Iva,Total):
        self.Autorizacion=Autorizacion
        self.Fecha=Fecha
        self.Referencia=Referencia
        self.Nit_Emisor=Nit_Emisor
        self.Nit_Receptor=Nit_Receptor
        self.Valor=Valor
        self.Iva=Iva
        self.Total=Total

    #Metodos GET
    def getAutorizacion(self):
        return self.Autorizacion

    def getFecha(self):
        return self.Fecha

    def getReferencia(self):
        return self.Referencia

    def getNit_Emisor(self):
        return self.Nit_Emisor

    def getNit_Receptor(self):
        return self.Nit_Receptor

    def getValor(self):
        return self.Valor

    def getIva(self):
        return self.Iva

    def getTotal(self):
        return self.Total

    #Metodos SET
    def setAutorizacion(self,Autorizacion):
        self.Autorizacion= Autorizacion

    def setFecha(self,Fecha):
        self.Fecha = Fecha

    def setReferencia(self,Referencia):
        self.Referencia = Referencia

    def setNit_Emisor(self,Nit_Emisor):
        self.Nit_Emisor = Nit_Emisor

    def setNit_Receptor(self,Nit_Receptor):
        self.Nit_Receptor = Nit_Receptor

    def setValor(self,Valor):
        self.Valor = Valor

    def setIva(self,Iva):
        self.Iva = Iva

    def setTotal(self,Total):
        self.Total = Total