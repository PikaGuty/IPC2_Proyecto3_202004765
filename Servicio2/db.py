import xml.etree.cElementTree as ET
from xml.dom import minidom

class db():

    def insertar(lista):
        
        root = ET.Element("terrenos")

        for i in lista:

            doc = ET.SubElement(root, "DTE")
            ET.SubElement(doc, "AUTORIZACION").text=str(i[0])
            ET.SubElement(doc, "FECHA").text=str(i[1])
            ET.SubElement(doc, "REFERENCIA").text=str(i[2])
            ET.SubElement(doc, "NIT_EMISOR").text=str(i[3])
            ET.SubElement(doc, "NIT_RECEPTOR").text=str(i[4])
            ET.SubElement(doc, "VALOR").text=str(i[5])
            ET.SubElement(doc, "IVA").text=str(i[6])
            ET.SubElement(doc, "TOTAL").text=str(i[7])
        
        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
        with open(str('db')+".xml", "w") as f:
            f.write(xmlstr)

    def obtener(lista):
        tree = ET.parse('db.xml')
        root = tree.getroot()
        
        for DTE in root.findall('DTE'):
            autorizacion = DTE.find('AUTORIZACION').text.strip()
            tiempo = DTE.find('FECHA').text.strip()
            referencia = DTE.find('REFERENCIA').text.strip()
            nit_emisor = DTE.find('NIT_EMISOR').text.strip()
            nit_receptor = DTE.find('NIT_RECEPTOR').text.strip()
            valor = DTE.find('VALOR').text.strip()
            iva = DTE.find('IVA').text.strip()
            total = DTE.find('TOTAL').text.strip()
            
            #print(tiempo, referencia, nit_emisor, nit_receptor, valor, iva, total)
            lista.append([autorizacion,tiempo, referencia, nit_emisor, nit_receptor, valor, iva, total])

    def reiniciar():
        root = ET.Element("terrenos")
        
        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
        with open(str('db')+".xml", "w") as f:
            f.write(xmlstr)


#db.insertar('31/01/2021 16:54','C1556','737810K','8338815','12.00','1.44','13.44')
#lista=[]
#db.obtener(lista)
#db.reiniciar()