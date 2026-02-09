import ftplib

#credenciales FTP, la contraseña la cambian cada cierto tiempo
FTP_HOST = "127.0.0.1"
FTP_USER = "ftpdam"
FTP_PASS = ""

try:
    # conexión al servidor de FTP
    ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)

    #forzar codificación UNICODE
    ftp.encoding = "utf-8"                                                                       
    print (ftp.getwelcome ())

    #bajamos el fichero subido anteriormente y lo renombramos a bajado. txt
    # fichero_enServidor = "subido.txt"
    fichero_enServidor = input("Introduce el nombre del fichero a descargar (ejemplo.txt): ")
    fichero_local = "bajado.txt"

    with open (fichero_local, "wb") as file:

    # usamos el comando RETR para descargar
        ftp.retrbinary(f"RETR {fichero_enServidor}", file.write)
        print('Descargado el fichero:', fichero_local)

    #cerrar la conexión
    ftp. quit()

except Exception as e:
    print("ERROR:", repr(e))