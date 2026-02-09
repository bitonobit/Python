import ftplib

# Importante: ejecutar este script en el directorio donde se encuentra el fichero a subir, para comprobarlo usa las tres lineas siguientes
# import os
# print("Directorio actual:", os.getcwd())
# print("Ficheros:", os.listdir())

#creadenciales FTP, la contraseña la cambian cada cierto tiempo
FTP_HOST = "127.0.0.1"
FTP_USER = "ftpdam"
FTP_PASS = ""

def listCallback (line):
    print(line)

try:
    # conexión al servidor de FTP
    ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
    
    #forzar codificación UNICODE
    ftp.encoding="utf-8"
    
    welcomeMessage = ftp.getwelcome()
    print (welcomeMessage)

    #fichero a subir
    # filename = "subido.txt"
    filename = input("Introduce el nombre del fichero a subir (ejemplo.txt): ")
    print("Abriendo fichero local...")
    with open(filename, "rb") as file:
        print("Subiendo fichero...")
        ftp.storbinary(f"STOR {filename}", file)
        print("Subida terminada")

    # listamos el contenido para comprobar
    print("PWD:", ftp.pwd())
    ftp.dir(listCallback)

    #cerrar la conexión
    ftp.quit()

except Exception as e:
    print("ERROR:", repr(e))