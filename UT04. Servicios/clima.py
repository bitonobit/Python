from urllib import request, error
import json
from getpass import getpass
import sys

def clima():
    print("El tiempo en tu cualquier lugar del mundo")
    print("____________________________________")
    lat = input("Introduce latitud: ")
    lon = input("Introduce longitud: ")
    apiKey = input("Introduce La API_Key: ")
    part = "hourly,daily"
    url=f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&exclude={part}&appid={apiKey}"
  
    try:
        # print(url)
        respuesta = request.urlopen(url)
        datos = respuesta.read().decode("utf-8")
        datos_json = json.loads(datos)

        print(f"Ciudad: {datos_json["name"]}")
        print("____________________________")
        print(f"Temperatura mínima: {datos_json["main"]["temp_min"]} ºC")
        print(f"Temperatura máxima: {datos_json["main"]["temp_max"]} ºC")
        print(f"Humedad: {datos_json["main"]["humidity"]} %")
        print(f"Cielo: {datos_json["weather"][0]["description"]}") 

    except error.HTTPError as e:
        if e.code == 404:
            print("\nError: No se ha encontrado la ciudad. Revisa el nombre.")
        elif e.code == 401:
            print("\nError: La API Key no es válida.")
        else:
            print(f"\nError HTTP: {e.code}")
        sys.exit()
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}")
        sys.exit()

if __name__ == "__main__":
    clima()
