# Ejemplo de obtención de la IP propia de un host
import socket

host = socket.gethostname() # obtener nombre del equipo
ip = socket.gethostbyname(host) # obtener dirección IP
print ("Nombre del equipo: %s" %host)
print ("Dirección IP: %s" %ip)