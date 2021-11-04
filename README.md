# IPC2_Proyecto3_202004765

La Superintendencia de Administración Tributaria le ha solicitado construir un software que
pueda ser consumido desde Internet como un servicio. Este software recibirá un mensaje
con los datos para solicitar la autorización de un Documento Tributario Electrónico (DTE)
emitido por un contribuyente y como respuesta emitirá un número único de autorización,
este número será un correlativo que iniciará con el valor 1 cada día y no deberá repetirse
de nuevo en ese día. La estructura del número de autorización es la siguiente:
yyyymmdd########, donde:
yyyy corresponde al año en que se solicita la autorización
mm corresponde al mes en que se solicita la autorización
dd corresponde al día en que se solicita la autorización
######## corresponde al correlativo precedido por la cantidad de 0’s necesarios
para mantener el formato: Ej. Para el correlativo 1: 00000001.
