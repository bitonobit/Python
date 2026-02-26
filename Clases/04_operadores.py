# *************************************************
#            Operadores Aritméticos
# *************************************************
# Operator	    Name	           Ejemplo
#   +	          Suma       	        x + y	
#   -	          Resta	              x - y	
#   *	          Multiplicación	    x * y	
#   /	          División	          x / y	
#   %	          Módulo	            x % y	
#   **          Exponenciación	    x ** y	
#   //          Floor división	    x // y

x1=2+3
x2=5-4
x3=2*8
x4=6/3
x5=8%2
x6=3**2
x7= 7//2

# *************************************************
#           Operadores de cancatenación
# *************************************************
# Operadores
nombre='Candy'
apellido='González'
nombreCompleto= nombre + ' ' + apellido     # Concatenar 
# NO se puede concatenar un cadena y un número, 
# en su lugar se usa f{} para formatear cadenas
edad = 51
saludo = f"Mi nombre es Candy y tengo {edad} años"
print(saludo)

# Formateando un float
pi=3.1415
res=f"El valor de pi es {pi:.2f}"   #.2f son sólo 2 decimales
print(res)
res=f"El valor de pi es {10 *5}"    # Se pueden hacer operaciones matemáticas incluso se pueden llamar funciones 

# *************************************************
#           Operadores de asignación
# *************************************************
# Operador	    Ejemplo	    Igual a	 
#   =	          x = 5	    x = 5	
#   +=	        x += 3	    x = x + 3	
#   -=	        x -= 3	    x = x - 3	
#   *=	        x *= 3	    x = x * 3	
#   /=	        x /= 3	    x = x / 3	
#   %=	        x %= 3	    x = x % 3	
#   //= 	      x //= 3	    x = x // 3	
#   **= 	      x **= 3	    x = x ** 3	
#   &=	        x &= 3	    x = x & 3	
#   |=	        x |= 3	    x = x | 3	
#   ^=	        x ^= 3	    x = x ^ 3	
#   >>= 	      x >>= 3	    x = x >> 3	
#   <<= 	      x <<= 3	    x = x << 3

# **********************************************
#     Operadores de comparación
# **********************************************
# Operador	    Nombre	            Ejemplo	 
#   ==      	Igual	            x == y	
#   !=      	Diferente	        x != y	
#   >	        Mayor que	        x > y	
#   <	        Menor que	        x < y	
#   >=      	Mayor o igua que	x >= y	
#   <=      	Menor o igua que	x <= y

# *******************************************************************************
#                         Operadores de lógicos
# *******************************************************************************
# Operador	    Descripción	                                    Ejemplo
#   and 	    Retorna verdad si ambos son verdad      	x < 5 and  x < 10	
#   or	        Retorna verdad si uno es verdad         	x < 5 or x < 4	
#   not	        Negación                                	not(x < 5 and x < 10)

# *******************************************************************************
#                         Operadores de identidad
# *******************************************************************************
# Operador	    Descripción	                                        Ejemplo
#   is 	        Devuelve verdad si ambas son el mismo objeto         x is y	
#   is not	    Devuelve verdad si ambas NO son el mismo objeto      x is not y	

# ********************************************************************************
#                         Operadores de membresía
# ********************************************************************************
#   Los operadores de membresía se utilizan para probar si una secuencia se presenta en un objeto:

# Operador	    Descripción	                            Ejemplo
#   in 	        Devuelve True si está presente	        x in y	
#   not in	    Devuelve True si NO está presente     x not in y	

# ********************************************************************************
#                         Operadores bit a bit 
# ********************************************************************************
# Los operadores bit a bit se utilizan para comparar números (binarios):

# Operador  Nombre	                Descripción	                                                Ejemplo
#   & 	    AND	                    Establece cada bit en 1 si ambos bits son 1	                x & y	
#   |	    OR	                    Establece cada bit en 1 si uno de los dos bits es 1	        x | y	
#   ^	    XOR	                    Establece cada bit en 1 si sólo uno de los dos bits es 1	x ^ y	
#   ~	    NOT	                    Invierte todos los bits	                                    ~x	
#   <<	    Zero fill left shift	Shift left by pushing zeros in from the right and let the leftmost bits fall off	x << 2	
#   >>	    Signed right shift	    Shift right by pushing copies of the leftmost bit in from the left, and let the rightmost bits fall off
