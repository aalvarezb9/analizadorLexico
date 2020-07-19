# Analizador léxico de algunos componentes del lenguajes C/C++
# Se hizo este analizador en base a los princiíos de automátas finitos y siguiendo diagramas de estado
# Lectura carácter por carácter del texto de entrada
# Señala errores y la línea en que se cometieron
#*************************HECHO POR: Ángel René Álvarez Banegas****************************************
#***********************************20171005063********************************************************


from Core.analisisLexico import *

analizador = (Analizador()).leerEntrada().automata()
print("\t\t\tTabla de tokens")
print("  TOKEN \t    DESCRIPCIÓN \t\t TIPO")
print(tabulate(analizador))