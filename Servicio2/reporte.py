import xml.etree.cElementTree as ET
from xml.dom import minidom

class db():
    def insertar():
        hola='hola'
        root = ET.Element("terrenos")

        doc = ET.SubElement(root, "DTE")

        ET.SubElement(doc, "AUTORIZACION").text=str(hola)

        ET.SubElement(doc, "FECHA").text=str(hola)

        ET.SubElement(doc, "REFERENCIA").text=str(hola)

        ET.SubElement(doc, "NIT_EMISOR").text=str(hola)

        ET.SubElement(doc, "NIT_RECEPTOR").text=str(hola)

        ET.SubElement(doc, "VALOR").text=str(hola)

        ET.SubElement(doc, "IVA").text=str(hola)

        ET.SubElement(doc, "TOTAL").text=str(hola)
        

        
        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
        with open(str(hola)+".xml", "w") as f:
            f.write(xmlstr)

db.insertar()