# Ejemplo de servidor TCP que recibe datos y responde, recibe datos del cliente hasta que recibe "0" o se desconecta
import socket

HOST = ''  # todas las interfaces locales a la escucha
PORT = 2000        # Puerto de escucha

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind((HOST, PORT))
  s.listen()
  conn, addr = s.accept() #línea bloqueante
  with conn:
    print(f"Conexión exitosa con el cliente. IP ({addr[0]}) Puerto ({addr[1]})")
    while True:
      data = conn.recv(1024) #línea bloqueante (Se detiene hasta recibir datos)
      print (data)
      if data==b"0":
        break
      conn.sendall(b"mensaje recibido")