#-*- coding: utf-8 -*-

import sys

class Analizador:
    def __init__(self):
        self.errores = {1: "No se ha selecciona un programa de entrada", 2: "Carácter desconocido en la línea: "}
        self.arreglo = []
        self.palabrasValidas = {"add": "add", "float": "float", "return": "return", "std": "std", "cout": "cout", "main": "main", "class": "class"}
        self.valoresEncontrados = []
        self.linea = 1
        self.inicio = 0
        self.e1 = 1
        self.e2 = 2
        self.e3 = 3
        self.estadoActual = self.inicio
        self.subEstado = self.inicio

    def leerEntrada(self):
        parametro = sys.argv[1:]

        if len(parametro) != 1:
            quit("Error: %s" % self.errores[1])
        self.nombreArchivo = parametro[0]
        archivo = open(self.nombreArchivo, "r")
        self.contenidoArchivo = archivo.read()
        archivo.close()

        return self

    def preparar(self):
        for i in range(len(self.contenidoArchivo)):
            self.arreglo.append(self.contenidoArchivo[i])

        # self.arreglo = self.eliminarElementoDeArreglo(self.arreglo, ' ')
        print(self.arreglo)

    def eliminarElementoDeArreglo(self, arr, elementoAEliminar):
        arrRetorno = []
        for i in range(len(arr)):
            if(arr[i] != elementoAEliminar):
                arrRetorno.append(arr[i])

        return arrRetorno

    def automata(self):
        self.it = 1
        for i in range(len(self.contenidoArchivo)):
            # self.trans = [lambda: self.contenidoArchivo[i - 1], lambda: self.contenidoArchivo[i]][i == 0]()
            self.trans = self.contenidoArchivo[i]
            self.valoresEncontrados.append(self.trans)
            print(self.trans + " --- %d" % i)
            self.estAnt = self.estadoActual
            if self.estadoActual == self.inicio:
                # self.valoresEncontrados.append(self.trans)
                if not self.trans.isdigit() and self.trans.isalnum(): #Es letra
                    self.puntoPartida = i
                    if self.trans == 'a':
                        self.estadoActual = 'AE1'
                    elif self.trans == 'c':
                        self.estadoActual = 'CA1'
                    elif self.trans == 'f':
                        self.estadoActual = 'F1'
                    elif self.trans == 's':
                        self.estadoActual = 'S1'
                    elif self.trans == 'r':
                        self.estadoActual = 'R1'
                    elif self.trans == 'i':
                        self.estadoActual = 'I1'
                    else:
                        self.estadoActual = 'V2'  
                elif self.trans.isdigit():
                    self.estadoActual = 'D' #Digito
                elif self.trans == ' ' or self.trans == '\n':
                    pass
                else: #Símbolo
                    if self.trans == '#':
                        self.estadoActual = 'G'
                    elif self.trans == '(':
                        print("Se encontró un inicio de agrupación: %s" % self.trans)
                        self.estadoActual = 'PP'
                    elif self.trans == '{':
                        print("Se encontró un inicio de apertura de statements: %s" % self.trans)
                        self.estadoActual = 'AS'
                    elif self.trans == '<<':
                        print("Se encontró el símbolo: %s" % self.trans)
                        self.estadoActual = "MQ"
                    elif self.trans == '\"':
                        print("Se encontró la apertura de un string con comillas dobles: %s" % self.trans)
                        self.estadoActual = 'STRR'
                    elif self.trans == ',':
                        print("Se encontró el separador de variables: %s" % self.trans)
                        self.estadoActual = 'CMM'
                    elif self.trans == '\'':
                        print("Se encontró el inicio de un string con comillas simples: %s" % self.trans)
                        self.estadoActual = 'STR'
                    elif self.trans == ')':
                        print("Se encontró el fin de una agrupación: %s" % self.trans)
                        self.estadoActual = 'FIN'
                    elif self.trans == '}':
                        print("Se encontró el fin de un statement: %s" % self.trans)
                        self.estadoActual = 'FIN'
                    elif self.trans == '=':
                        self.estadoActual = 'OA'
                    elif self.trans == ';':
                        print("Se encontró el fin de una instrucción: %s" % self.trans)
                    elif self.trans == '+':
                        self.estadoActual = 'ACUM'
                    elif self.trans == '-':
                        print("Se encontró el operador de resta: %s" % self.trans)
                    elif self.trans == '*':
                        print("Se encontró el operador de multiplicación: %s" % self.trans)
                    elif self.trans == '/':
                        print("Se encontró el operador de división: %s" % self.trans)
                    elif self.trans == ' ':
                        pass
                    else:
                        quit("Error: símbolo desconocido")


            elif self.estadoActual == 'L':
                # self.valoresEncontrados.append(self.trans)
                if self.trans == 'a':
                    self.estadoActual = 'AE1'
                elif self.trans == 'c':
                    self.estadoActual = 'CA1'
                elif self.trans == 'f':
                    self.estadoActual = 'F1'
                elif self.estadoActual == 's':
                    self.estadoActual = 'S1'
                elif self.trans == 'r':
                    self.estadoActual = 'R1'
                elif self.trans == 'i':
                    self.estadoActual = 'I1'
                else: 
                    self.estadoActual = 'V'
            elif self.estadoActual == 'AE1':
                if self.trans == 'd':
                    self.estadoActual = 'AE2'
                    # self.valoresEncontrados.append(self.trans)
                else:
                    self.estadoActual = 'V2'
                    
            elif self.estadoActual == 'AE2':
                if self.trans == 'd':
                    self.estadoActual = 'FIN'
                    print("Se encontró la palabra reservada %s " % self.palabrasValidas["add"])
                    # self.valoresEncontrados.append(self.trans)
                else:
                    self.estadoActual = 'V2'
                    
            elif self.estadoActual == 'CA1':
                if self.trans == 'l':
                    self.estadoActual = 'CL1'
                    # self.valoresEncontrados.append(self.trans)
                elif self.trans == 'o':
                    self.estadoActual = 'CO1'
                    # self.valoresEncontrados.append(self.trans)
                else:
                    self.estadoActual = 'V2'
                    
            elif self.estadoActual == 'CL1':
                if self.trans == 'a':
                    self.estadoActual = 'CL2'
                    # self.valoresEncontrados.append(self.trans)
                else:
                    self.estadoActual = 'V2'
                    
            elif self.estadoActual == 'CL2':
                if self.trans == 's':
                    self.estadoActual = 'CL3'
                    # self.valoresEncontrados.append(self.trans)
                else:
                    self.estadoActual = 'V2'
                    
            elif self.estadoActual == 'CL3':
                if self.trans == 's':
                    self.estadoActual = 'FIN'
                    print("Se encontró la palabra reservada %s" % self.palabrasValidas["class"])
                    # self.valoresEncontrados.append(self.trans)
                else:
                    self.estadoActual = 'V2'
                    
            elif self.estadoActual == 'CO1':
                if self.trans == 'u':
                    self.estadoActual = 'CO2'
                    # self.valoresEncontrados.append(self.trans)
                else:
                    self.estadoActual = 'V2'
                    
            elif self.estadoActual == 'CO2':
                if self.trans == 't':
                    self.estadoActual = 'FIN'
                    print("Se encontró la palabra reservada %s" % self.palabrasValidas["cout"])
                    # self.valoresEncontrados.append(self.trans)
                else:
                    self.estadoActual = 'V2'
                    
            elif self.estadoActual == 'F1':
                if self.trans == 'l':
                    self.estadoActual = 'F2'
                    # self.valoresEncontrados.append(self.trans)
                else:
                    self.estadoActual = 'V2'
                    
            elif self.estadoActual == 'F2':
                if self.trans == 'o':
                    self.estadoActual = 'F3'
                    # self.valoresEncontrados.append(self.trans)
                else:
                    self.estadoActual = 'V2'
                    
            elif self.estadoActual == 'F3':
                if self.trans == 'a':
                    self.estadoActual = 'F4'
                    # self.valoresEncontrados.append(self.trans)
                else:
                    self.estadoActual = 'V2'
                    
            elif self.estadoActual == 'F4':
                if self.trans == 't':
                    self.estadoActual = 'FIN'
                    print("Se encontró la palabra reservada para tipo de dato %s" % self.palabrasValidas["float"])
                    # self.valoresEncontrados.append(self.trans)
                else:
                    self.estadoActual = 'V2'
                    
            elif self.estadoActual == 'S1':
                if self.trans == 't':
                    self.estadoActual = 'S2'
                    # self.valoresEncontrados.append(self.trans)
                else:
                    self.estadoActual = 'V2'
                    
            elif self.estadoActual == 'S2':
                if self.trans == 'd':
                    self.estadoActual = 'FIN'
                    print("Se encontró la palabra reservada para salida de texto %s" % self.palabrasValidas["std"])
                    # self.valoresEncontrados.append(self.trans)
                else:
                    self.estadoActual = 'V2'
                    
            elif self.estadoActual == 'R1':
                if self.trans == 'e':
                    self.estadoActual = 'R2'
                    # self.valoresEncontrados.append(self.trans)
                else:
                    self.estadoActual = 'V2'
                    
            elif self.estadoActual == 'R2':
                if self.trans == 't':
                    self.estadoActual = 'R3'
                    # self.valoresEncontrados.append(self.trans)
                else:
                    self.estadoActual = 'V2'
                    
            elif self.estadoActual == 'R3':
                if self.trans == 'u':
                    self.estadoActual = 'R4'
                    # self.valoresEncontrados.append(self.trans)
                else:
                    self.estadoActual = 'V2'
                    
            elif self.estadoActual == 'R4':
                if self.trans == 'r':
                    self.estadoActual = 'R5'
                    # self.valoresEncontrados.append(self.trans)
                else:
                    self.estadoActual = 'V2'
                    
            elif self.estadoActual == 'R5':
                if self.trans == 'n':
                    self.estadoActual = 'FIN'
                    print("Se encontró la palabra reservada para retornar dato %s" % self.palabrasValidas["return"])
                    # self.valoresEncontrados.append(self.trans)
                else:
                    self.estadoActual = 'V2'
                    
            elif self.estadoActual == 'I1':
                if self.trans == 'n':
                    self.estadoActual = 'I2'
                    # self.valoresEncontrados.append(self.trans)
                else:
                    self.estadoActual = 'V2'
                    
            elif self.estadoActual == 'I2':
                if self.trans == 't':
                    self.estadoActual = 'FIN'
                    print("Se encontró la palabra reservada para reservar dato entero %s" % "int")
                    # self.valoresEncontrados.append(self.trans)
                else:
                    self.estadoActual = 'V2'
                    
            #Identificador de usuario
            elif self.estadoActual == 'V':
                if self.estAnt == self.inicio: #estAnt guarda el estado anterior, si es 0, es porque va iniciando una línea
                    self.estadoActual = 'V2'
                    # self.valoresEncontrados.append(self.trans)
                else:
                    self.estadoActual = 'V2'
                    # self.valoresEncontrados.append(self.trans)
            elif self.estadoActual == 'V2':
                if self.trans.isalnum(): 
                    self.estadoActual = 'V2'
                    # print("Se encontró el identificador de usuario: %s" % self.nombreID(self.puntoPartida, i))
                elif self.trans == '=':
                    self.estadoActual = 'FIN'
                    print("Se encontró el operador de asignación: %s" % self.trans)
                elif self.trans == ';':
                    self.estadoActual = 'FIN'
                    print("Se encontró el fin de una instrucción: %s" % self.trans)
                elif self.trans == '\n':
                    self.estadoActual = 'FIN'
                    print("Se encontró el identificador de usuario: %s" % self.nombreID(self.puntoPartida, i))
                elif self.trans == ' ':
                    self.estadoActual = 'FIN'
                    print("Se encontró el identificador de usuario: %s" % self.nombreID(self.puntoPartida, i))
                elif not self.trans.isalnum():
                    if self.trans == '_':
                        self.estadoActual = 'V2'
                    else:
                        quit("Error, token desconocido")
                else:
                    self.estadoActual = 'V2'

            elif self.estadoActual == 'D':
                if self.trans == ';':
                    self.estadoActual = 'FIN'
                    print("Se encontró el fin de una instrucción: %s" % self.trans)
                elif not self.trans.isdigit():
                    self.estadoActual = 'L'
                elif self.trans == ' ':
                    pass
                elif self.trans.isdigit():
                    self.estadoActual = 'D'
                elif self.trans == '.':
                    self.estadoActual = 'FL'
                else:
                    self.estadoActual = 'FIN'
            elif self.estadoActual == 'FL':
                if self.trans.isdigit():
                    self.estadoActual = 'FL'
                elif not self.trans.isdigit() and self.trans.isalnum():
                    self.estadoActual = 'L'
                elif self.trans == ';':
                    self.estadoActual = 'FIN'
                    print("Se encontró el fin de una instrucción: %s" % self.trans)
                else:
                    pass
            
            elif self.estadoActual == 'G':
                if self.trans == 'i':
                    self.estadoActual = 'GII'
                    # if self.trans == 'n':
                    #     self.estadoActual = 'GN1'
                    # elif self.trans == 'f':
                    #     self.estadoActual = 'GF1'
                    # else:
                    #     self.imprimirError1()
                elif self.trans == 'd':
                    self.estadoActual = 'GD1'
                elif self.trans == 'e':
                    self.estadoActual = 'GE1'
            elif self.estadoActual == 'GII':
                if self.trans == 'n':
                    self.estadoActual = 'GN1'
                elif self.trans == 'f':
                    self.estadoActual = 'GF1'
                else:
                    self.imprimirError1()
            elif self.estadoActual == 'GN1':
                if self.trans == 'c':
                    self.estadoActual = 'GN2'
                else:
                    self.imprimirError1()
            elif self.estadoActual == 'GN2':
                if self.trans == 'l':
                    self.estadoActual = 'GN3'
                else:
                    self.imprimirError1()
            elif self.estadoActual == 'GN3':
                if self.trans == 'u':
                    self.estadoActual = 'GN4'
                else:
                    self.imprimirError1()
            elif self.estadoActual == 'GN4':
                if self.trans == 'd':
                    self.estadoActual = 'GN5'
                else:
                    self.imprimirError1()
            elif self.estadoActual == 'GN5':
                if self.trans == 'e':
                    self.estadoActual = 'FIN'
                    print("Se encontró la directiva #include")
                else:
                    self.imprimirError1()
            elif self.estadoActual == 'GF1':
                if self.trans == 'n':
                    self.estadoActual = 'GF2'
                else:
                    self.imprimirError1()
            elif self.estadoActual == 'GF2':
                if self.trans == 'd':
                    self.estadoActual = 'GF3'
                else:
                    self.imprimirError1()
            elif self.estadoActual == 'GF3':
                if self.trans == 'e':
                    self.estadoActual = 'GF4'
                else:
                    self.imprimirError1()
            elif self.estadoActual == 'GF4':
                if self.trans == 'f':
                    self.estadoActual = 'FIN'
                    print("Se encontró la directiva ifndef")
                else:
                    self.imprimirError1()

            elif self.estadoActual == 'GD1':
                if self.trans == 'e':
                    self.estadoActual = 'GD2'
                else:
                    self.imprimirError1()
            elif self.estadoActual == 'GD2':
                if self.trans == 'f':
                    self.estadoActual = 'GD3'
                else:
                    self.imprimirError1()
            elif self.estadoActual == 'GD3':
                if self.trans == 'i':
                    self.estadoActual = 'GD4'
                else:
                    self.imprimirError1()
            elif self.estadoActual == 'GD4':
                if self.trans == 'n':
                    self.estadoActual = 'GD5'
                else:
                    self.imprimirError1()
            elif self.estadoActual == 'GD5':
                if self.trans == 'e':
                    self.estadoActual = 'FIN'
                    print("Se encontró la directiva #define")
                else:
                    self.imprimirError1()

            elif self.estadoActual == 'GE1':
                if self.trans == 'n':
                    self.estadoActual = 'GE2'
                else:
                    self.imprimirError1()
            elif self.estadoActual == 'GE2':
                if self.trans == 'd':
                    self.estadoActual = 'GE3'
                else:
                    self.imprimirError1()
            elif self.estadoActual == 'GE3':
                if self.trans == 'i':
                    self.estadoActual = 'GE4'
                else:
                    self.imprimirError1()
            elif self.estadoActual == 'GE4':
                if self.trans == 'f':
                    self.estadoActual == 'FIN'
                    print("Se encontró la directiva #endif")
                else:
                    self.imprimirError1()

            elif self.estadoActual == 'PP':
                if self.trans.isdigit():
                    self.estadoActual = 'D'
                elif not self.trans.isdigit() and self.trans.isalnum():
                    self.puntoPartida = i
                    if self.trans == 'a':
                        self.estadoActual = 'AE1'
                    elif self.trans == 'c':
                        self.estadoActual = 'CA1'
                    elif self.trans == 'f':
                        self.estadoActual = 'F1'
                    elif self.estadoActual == 's':
                        self.estadoActual = 'S1'
                    elif self.trans == 'r':
                        self.estadoActual = 'R1'
                    elif self.trans == 'i':
                        self.estadoActual = 'I1'
                    else: 
                        self.estadoActual = 'V2'
                else: #Símbolo
                    if self.trans == '#':
                        self.estadoActual = 'G'
                    elif self.trans == '(':
                        print("Se encontró un inicio de agrupación: %s" % self.trans)
                        self.estadoActual = 'PP'
                    elif self.trans == '{':
                        print("Se encontró un inicio de apertura de statements: %s" % self.trans)
                        self.estadoActual = 'AS'
                    elif self.trans == '<<':
                        print("Se encontró el símbolo: %s" % self.trans)
                        self.estadoActual = "MQ"
                    elif self.trans == '\"':
                        print("Se encontró la apertura de un string con comillas dobles: %s" % self.trans)
                        self.estadoActual = 'STRR'
                    elif self.trans == ',':
                        print("Se encontró el separador de variables: %s" % self.trans)
                        self.estadoActual = 'CMM'
                    elif self.trans == '\'':
                        print("Se encontró el inicio de un string con comillas simples: %s" % self.trans)
                        self.estadoActual = 'STR'
                    elif self.trans == ')':
                        print("Se encontró el fin de una agrupación: %s" % self.trans)
                        self.estadoActual = 'FIN'
                    elif self.trans == '}':
                        print("Se encontró el fin de un statement: %s" % self.trans)
                        self.estadoActual = 'FIN'
                    elif self.trans == '=':
                        self.estadoActual = 'OA'
                    elif self.trans == ';':
                        print("Se encontró el fin de una instrucción: %s" % self.trans)
                    elif self.trans == '+':
                        self.estadoActual = 'ACUM'
                    elif self.trans == '-':
                        print("Se encontró el operador de resta: %s" % self.trans)
                        self.estadoActual = 'FIN'
                    elif self.trans == '*':
                        print("Se encontró el operador de multiplicación: %s" % self.trans)
                        self.estadoActual = 'FIN'
                    elif self.trans == '/':
                        print("Se encontró el operador de división: %s" % self.trans)
                        self.estadoActual = 'FIN'
                    else:
                        quit("Error: símbolo desconocido")

            elif self.estadoActual == 'OA':
                if self.trans == '=':
                    print("Se encontró el operador de comparación: =%s" % self.trans)
                    self.estadoActual = 'FIN'
                self.estadoActual = 'FIN'
            elif self.estadoActual == 'ACUM':
                if self.trans == '=':
                    print("Se ha encontrado el operador de acumulación: +%s" % self.trans)
                    self.estadoActual = 'FIN'
                self.estadoActual = 'FIN'

            #identificación de string con comillas dobles
            elif self.estadoActual == 'STRR':
                if self.trans == '\"':
                    print("Se ha reconocido el fin de un string de comillas dobles: %s" % self.contenidoArchivo[i - 1])
                    self.estadoActual = 'FIN'
                elif self.trans == '\n':
                    quit("Error, comillas no cerradas: %s" % self.trans)
                else:
                    self.estadoActual = 'STRR'

            #identificación de string con comillas simples
            elif self.estadoActual == 'STR':
                if self.trans == '\'':
                    print("Se ha reconocido el fin de un string de comillas simples: %s" % self.trans)
                    self.estadoActual = 'FIN'
                elif self.trans == '\n':
                    quit("Error, comillas no cerradas: %s" % self.contenidoArchivo[i - 1])
                else:
                    self.estadoActual = 'STR'

            elif self.estadoActual == 'FIN':
                self.estadoActual = self.inicio
            

        print(self.valoresEncontrados)

    def imprimirError1(self):
        quit("Error: definición de directiva no pertenece al léxico")
                        
    def nombreID(self, inicio, fin):
        arregloID = []
        for i in range(inicio, fin):
            arregloID.append(self.contenidoArchivo[i])
        return "".join(arregloID)
    
    
    


    # def preparar(self):
    #     conteidoArchivo = self.contenidoArchivo
    #     conteidoArchivo = self.contenidoArchivo.replace(";", " ; ")
    #     conteidoArchivo = self.contenidoArchivo.replace("=", " = ")

    #     self.contenidoArchivo = ("%s".strip() % conteidoArchivo).strip()
        
    #     return self

    # def eliminarEspacios(self, cadena):
    #     for i in range(len(cadena)):
    #         if(cadena[i] == '\t')

(Analizador()).leerEntrada().automata()