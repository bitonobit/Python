# *****************************************************************************
#                          Listas
# Los elementos de la lista son modificables y permiten valores duplicados.
#*******************************************************************************
lista = ["Candy", "Glez", "Bitonobit"]
# Una lista puede contener diferentes tipos de datos:
lista = [1, True, "Bitonobit"]
var= list(("Candy", "Glez", "Bitonobit")) # Constructor de list debes agregar doble (())
# Si tiene una colección de valores en una lista, tupla, etc. Python le permite extraer los valores en variables.
# A esto se le llama desempacar .
nombres = ["Ana", "Pedro", "Juan"]
x, y, z = nombres
print(x)
print(y)
print(z)
# También podría ser:
print(x, y, z)
a=[1,2,3,4,5,6,7,8,9,10]
print(a[0])     # Muestra el valor en la posición 0 -> 1
print(a[-1])    # Muestra el valor en la última posición -> 5
a[-1]=100       #Cambiar un valor

# Al especificar un rango, el valor de retorno será una nueva lista con los elementos especificados.
print(a[2:5]) #comienza en 2 incluido y termina en 4 porque no incluye el 5
print(a[:5])  #comienza desde cero
print(a[4:])  #comienza desde 4 hasta el final de la cadena
print(a[-5:-2]) 

a[1:3]=["a","b"]  # Cambiar un rango de valores 
print(a)

# Buscar un valor en la lista
if 5 in a:        
  print("Sip, 5 está en la lista")    

#******************************************************************************
#                         Métodos de Listas
#******************************************************************************
len(a)                  # Cuenta el número de elementos de la lista
a.insert(2, "x")        # Inserta el caracter x en la posición 2
a.append("y")           # Inserta el caracter x en la última posición
b=[22,44,33,67]
a.extend(b)             # Agregar elementos de otra lsita
d= a + b                # Otra forma de unir dos listas
print(a)
# El extend()método no tiene que agregar listas , puede agregar cualquier objeto iterable
c=(99,98,97)
a.extend(c)
a.remove(97)              # Remueve un elemento especificado
a.remove("x")             # Remueve la primera aparición de x
a.pop(2)                  # Remueve el elemento en la posición 2
a.pop()                   # Remueve el último elemento 
del a[5]                  # Remueve el elemento en la posición 5
#del a                    # Elimina la lista por completo
#a.clear()                # Limpia la lista
a.index(22)               # Devuelve el índice del elemento encontrado
nElementos=a.count("x")   # Cuenta el número de ocurrencias de un elemento
b.sort()                  # Ordena una lista ascendentemente
b.sort(reverse = True)    # Ordena una lista descendentemente
b = a.copy()              # Copiar una lista
c = list(b)               # Otra forma de copiar una lista

# Recorrer la lista
for x in a:
  print(x)

# Recorrer un rango de la lista
for x in range(3,5):
  print(x)

#  Crear una lista a partir de otra con una condición. Ejemplo que el nombre contenga una e
alumnos = ["Ana", "Pedro", "Juan", "Rafael", "Alejandro"]
nuevaLista = []

for x in alumnos:
  if "e" in x:
    nuevaLista.append(x)

print(nuevaLista)

# Usando comprensión de lista sería más corto de escribir
otraLista = [x for x in alumnos if "e" in x]
print(otraLista)
# Sintaxis: newlist = [expression for item in iterable if condition == True]

num = [x for x in range(10)]      # Crea una lista con números del 1 al 10

listaMayusculas = [x.upper() for x in alumnos]    # Crea los valores de la nueva lista en mayúsculas

# Condicionar la creación de la lista:
listaCondicionada = [x if x != "Ana" else "Rafael" for x in a]  #Cambia las Ana por Rafael
