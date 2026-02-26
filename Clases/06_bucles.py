#******************************************************************************
#                          Bucles
# ******************************************************************************
i = 0
while i < 10:
  print(i)
  i = i + 1

#  Se puede usar break y continue igual que en php o js
i = 1
while i < 5:
  print(i)
  i += 1
else:
  #Se ejecuta una vez cuando la condición ya no es verdadera
  print("i no es mayor que 5")        

# Bucles a través de una cadena
for x in "Bitonobit":
  print(x)

t=("a","b","c","d",25)
for i in range(len(t)):
  print(t[i])            #Recorre la tupla t3

a = ["Carlos", "Ana", "María", "Ana"]
for x in a:
  print(x)
  if x == "Ana":
    continue

for x in range(6):
  print(x)

for x in range(2, 6):
  print(x)

for x in range(1, 30, 3): #El tercer parámetro es el incremento
  print(x)                #Cuenta del 1 al 30, pero de 3 en 3
else:
  print("Terminé!")
  