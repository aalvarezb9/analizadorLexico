#-*- coding: utf-8 -*-
from tabulate import tabulate
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
        self.tokens = 0
        self.tokensEncontrados = []
        self.vvvv = []

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
                self.puntoPartida = i
                # self.valoresEncontrados.append(self.trans)
                if not self.trans.isdigit() and self.trans.isalnum(): #Es letra
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
                    elif self.trans == 'p':
                        self.estadoActual = 'P1'
                    else:
                        self.estadoActual = 'V2'  
                elif self.trans.isdigit():
                    self.estadoActual = 'D'
                elif self.trans == '\n':
                    self.linea += 1
                elif self.trans == ' ':
                    pass
                else: #Símbolo
                    if self.trans == '#':
                        self.estadoActual = 'G'
                    elif self.trans == '(':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Inicio agrupación", "Agrupación"]]
                        print("Se encontró un inicio de agrupación: %s" % self.trans)
                        self.estadoActual = 'PP'
                    elif self.trans == '{':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Inicio statement", "Agrupación"]]
                        print("Se encontró un inicio de apertura de statements: %s" % self.trans)
                        self.estadoActual = 'AS'
                    elif self.trans == '<':
                        self.estadoActual = 'MQ'
                    elif self.trans == '>':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Mayor que", "Comparación"]]
                        self.estadoActual = 'MYQ'
                    elif self.trans == '\"':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Inicio de string (comillas dobles)", "String"]]
                        print("Se encontró la apertura de un string con comillas dobles: %s" % self.trans)
                        self.estadoActual = 'STRR'
                    elif self.trans == ',':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Separador de datos", "Separador"]]
                        print("Se encontró el separador de variables: %s" % self.trans)
                        self.estadoActual = self.inicio
                    elif self.trans == '\'':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Inicio de string (comillas simples)", "String"]]
                        print("Se encontró el inicio de un string con comillas simples: %s" % self.trans)
                        self.estadoActual = 'STR'
                    elif self.trans == ')':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Fin de agrupación", "Agrupación"]]
                        print("Se encontró el fin de una agrupación: %s" % self.trans)
                        self.estadoActual = self.inicio
                    elif self.trans == ':':
                        self.estadoActual = 'DP'
                    elif self.trans == '.':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "LLama a métodos", "---"]]
                        self.estadoActual = self.inicio
                        print("Se ha encontrado el símbolo para añadir métodos: %s" % self.trans)
                    elif self.trans == '}':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Fin de un statement", "Agrupación"]]
                        print("Se encontró el fin de un statement: %s" % self.trans)
                        self.estadoActual = self.inicio
                    elif self.trans == '=':
                        self.estadoActual = 'OA'
                    elif self.trans == ';':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Fin de una instrucción", "Separador"]]
                        print("Se encontró el fin de una instrucción: %s" % self.trans)
                        self.estadoActual = self.inicio
                    elif self.trans == '+':
                        self.estadoActual = 'ACUM'
                    elif self.trans == '-':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Resta", "Operador"]]
                        print("Se encontró el operador de resta: %s" % self.trans)
                        self.estadoActual = self.inicio
                    elif self.trans == '*':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Multiplicación", "Operador"]]
                        print("Se encontró el operador de multiplicación: %s" % self.trans)
                        self.estadoActual = self.inicio
                    elif self.trans == '/':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "División", "Operador"]]
                        print("Se encontró el operador de división: %s" % self.trans)
                        self.estadoActual = self.inicio
                    elif self.trans == '\n':
                        self.linea += 1
                    elif self.trans == ' ' or self.trans == '\t':
                        pass
                    else:
                        quit("Error: símbolo desconocido: '%s' en la línea %d" % (self.trans, self.linea))


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
                    self.tokens += 1
                    self.estadoActual = self.inicio
                    self.tokensEncontrados += [["add", "Función", "Palabra reservada"]]
                    print("Se encontró la palabra reservada %s " % self.palabrasValidas["add"])
                    # self.valoresEncontrados.append(self.trans)
                else:
                    self.estadoActual = 'V2'

            elif self.estadoActual == 'P1':
                if self.trans == 'u':
                    self.estadoActual = 'P2'
                else:
                    self.estadoActual = 'V2'
            elif self.estadoActual == 'P2':
                if self.trans == 'b':
                    self.estadoActual = 'P3'
                else:
                    self.estadoActual = 'V2'
            elif self.estadoActual == 'P3':
                if self.trans == 'l':
                    self.estadoActual = 'P4'
                else:
                    self.estadoActual = 'V2'
            elif self.estadoActual == 'P4':
                if self.trans == 'i':
                    self.estadoActual = 'P5'
                else:
                    self.estadoActual = 'V2'
            elif self.estadoActual == 'P5':
                if self.trans == 'c':
                    self.tokens += 1
                    self.estadoActual = self.inicio
                    self.tokensEncontrados += [[self.nombreID(self.puntoPartida, i), "Define un tipo de dato/función", "Palabra reservada"]]
                    print("Se ha encontrado la palabra reservada par definir tipo de función: %s" % self.nombreID(self.puntoPartida, i))
                    
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
                    self.tokens += 1
                    self.estadoActual = self.inicio
                    self.tokensEncontrados += [["class", "Define una clase", "Palabra reservada"]]
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
                    self.tokens += 1
                    self.estadoActual = self.inicio
                    self.tokensEncontrados += [["cout", "Permite mostrar un texto", "Palabra reservada"]]
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
                    self.tokens += 1
                    self.estadoActual = self.inicio
                    self.tokensEncontrados += [["float", "Tipo de dato/función", "Palabra reservada"]]
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
                    self.tokens += 1
                    self.estadoActual = self.inicio
                    self.tokensEncontrados += [["std", "Permite la salida de texto con 'cout'", "Palabra reservada"]]
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
                    self.tokens += 1
                    self.estadoActual = self.inicio
                    self.tokensEncontrados += [["return", "Retorna un dato", "Palabra reservada"]]
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
                    self.tokens += 1
                    self.estadoActual = self.inicio
                    self.tokensEncontrados += [["int", "Tipo de dato", "Palabra reservada"]]
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
                    self.tokens += 1
                    self.estadoActual = self.inicio
                    self.tokensEncontrados += [[self.trans, "Asigna valor", "Operador"]]
                    print("Se encontró el operador de asignación: %s" % self.trans)
                elif self.trans == ';':
                    self.tokens += 1
                    self.estadoActual = self.inicio
                    self.tokensEncontrados += [[self.trans, "Finaliza una línea/instrucción", "Carácter"]]
                    print("Se encontró el fin de una instrucción: %s" % self.trans)
                elif self.trans == '\n':
                    self.linea += 1
                    self.tokens += 1
                    self.estadoActual = self.inicio
                    self.tokensEncontrados += [[self.nombreID(self.puntoPartida, i), "Define el nombre de un dato/función", "Identificador de usuario"]]
                    print("Se encontró el identificador de usuario: %s" % self.nombreID(self.puntoPartida, i))
                elif self.trans == ' ':
                    self.estadoActual = self.inicio
                    self.tokensEncontrados += [[self.nombreID(self.puntoPartida, i), "Define el nombre de un dato/función", "Identificador de usuario"]]
                    print("Se encontró el identificador de usuario: %s" % self.nombreID(self.puntoPartida, i))
                elif not self.trans.isalnum():
                    if self.trans == '_':
                        self.estadoActual = 'V2'
                    else:
                        self.tokens += 1
                        self.tokensEncontrados += [[self.nombreID(self.puntoPartida, i), "Define el nombre de un dato/función", "Identificador de usuario"]]
                        print("Se encontró un identificador de usuario: %s" % self.nombreID(self.puntoPartida, i))
                        if self.trans == '#':
                            self.estadoActual = 'G'
                        elif self.trans == '(':
                            self.tokens += 1
                            self.tokensEncontrados += [[self.trans, "Inicia una agrupación", "Agrupación"]]
                            print("Se encontró un inicio de agrupación: %s" % self.trans)
                            self.estadoActual = 'PP'
                        elif self.trans == '{':
                            self.tokens += 1
                            self.tokensEncontrados += [[self.trans, "Inicio de statement", "Agrupación"]]
                            print("Se encontró un inicio de apertura de statements: %s" % self.trans)
                            self.estadoActual = 'AS'
                        elif self.trans == '<':
                            self.estadoActual = 'MQ'
                        elif self.trans == '>':
                            self.estadoActual = 'MYQ'
                        elif self.trans == '\"':
                            self.tokens += 1
                            self.tokensEncontrados += [[self, "Inicia un string (comillas dobles)", "String"]]
                            print("Se encontró la apertura de un string con comillas dobles: %s" % self.trans)
                            self.estadoActual = 'STRR'
                        elif self.trans == ',':
                            self.tokens += 1
                            self.tokensEncontrados += [[self.trans, "Separación de variables", "Separador"]]
                            print("Se encontró el separador de variables: %s" % self.trans)
                            self.estadoActual = self.inicio
                        elif self.trans == '\'':
                            self.tokens += 1
                            self.tokensEncontrados += [[self.trans, "Inicia un string (comillas simples)", "String"]]
                            print("Se encontró el inicio de un string con comillas simples: %s" % self.trans)
                            self.estadoActual = 'STR'
                        elif self.trans == ')':
                            self.tokens += 1
                            self.tokensEncontrados += [[self.trans, "Finaliza una agrupación", "Agrupación"]]
                            print("Se encontró el fin de una agrupación: %s" % self.trans)
                            self.estadoActual = self.inicio
                        elif self.trans == ':':
                            self.estadoActual = 'DP'
                        elif self.trans == '.':
                            self.tokens += 1
                            self.tokensEncontrados += [[self.trans, "Llama a métodos", "---"]]
                            self.estadoActual = self.inicio
                            print("Se ha encontrado el símbolo para añadir métodos: %s" % self.trans)
                        elif self.trans == '}':
                            self.tokens += 1
                            self.tokensEncontrados += [[self.trans, "Finaliza un statement", "Agrupación"]]
                            print("Se encontró el fin de un statement: %s" % self.trans)
                            self.estadoActual = self.inicio
                        elif self.trans == '=':
                            self.estadoActual = 'OA'
                        elif self.trans == ';':
                            self.tokens += 1
                            self.tokensEncontrados += [[self.trans, "Finaliza una línea/instrucción", "Carácter"]]
                            print("Se encontró el fin de una instrucción: %s" % self.trans)
                            self.estadoActual = self.inicio
                        elif self.trans == '+':
                            self.estadoActual = 'ACUM'
                        elif self.trans == '-':
                            self.tokens += 1
                            self.tokensEncontrados += [[self.trans, "Resta", "Operador"]]
                            print("Se encontró el operador de resta: %s" % self.trans)
                            self.estadoActual = self.inicio
                        elif self.trans == '*':
                            self.tokens += 1
                            self.tokensEncontrados += [[self.trans, "Multiplicación", "Operador"]]
                            print("Se encontró el operador de multiplicación: %s" % self.trans)
                            self.estadoActual = self.inicio
                        elif self.trans == '/':
                            self.tokens += 1
                            self.tokensEncontrados += [[self.trans, "División", "Operador"]]
                            print("Se encontró el operador de división: %s" % self.trans)
                            self.estadoActual = self.inicio
                        elif self.trans == '\n':
                            self.linea += 1
                        elif self.trans == ' ' or self.trans == '\t':
                            pass
                        else:
                            quit("Error: símbolo desconocido: %s, en la línea %d" % (self.trans, self.linea))
                else:
                    self.estadoActual = self.inicio

            elif self.estadoActual == 'D':
                if self.trans == ';':
                    self.estadoActual = self.inicio
                    self.tokens += 2
                    self.tokensEncontrados += [[self.nombreID(self.puntoPartida, i), "Entero", "Número"]]
                    self.tokensEncontrados += [[self.trans, "Finaliza una línea/instrucción", "Carácter"]]
                    print("Se encontró al número entero: %s" % self.nombreID(self.puntoPartida, i).replace(";", ""))
                    print("Se encontró el fin de una instrucción: %s" % self.trans)
                if self.trans == '\n':
                    self.linea += 1
                    self.tokensEncontrados += [[self.nombreID(self.puntoPartida, i), "Entero", "Número"]]
                    print("Se encontró al número entero: %s" % self.nombreID(self.puntoPartida, i))
                    self.estadoActual = self.inicio
                elif self.trans == ' ':
                    self.tokens += 1
                    self.tokensEncontrados += [[self.nombreID(self.puntoPartida, i), "Entero", "Número"]]
                    print("Se encontró al número entero: %s" % self.nombreID(self.puntoPartida, i))
                    self.estadoActual = self.inicio
                elif not self.trans.isdigit():
                    self.tokens += 1
                    self.estadoActual = self.inicio
                    self.tokensEncontrados += [[self.nombreID(self.puntoPartida, i), "Entero", "Número"]]
                    print("Se encontró al número entero: %s" % self.nombreID(self.puntoPartida, i))
                elif self.trans.isdigit():
                    self.estadoActual = 'D'
                elif self.trans == '.':
                    self.estadoActual = 'FL'
                else:
                    self.estadoActual = self.inicio

            elif self.estadoActual == 'FL':
                if self.trans.isdigit():
                    self.estadoActual = 'FL'
                elif not self.trans.isdigit():
                    self.tokens += 1
                    self.tokensEncontrados += [[self.nombreID(self.puntoPartida, i), "Flotante", "Número"]]
                    print("Se encontró el número flotante: %s" % self.nombreID(self.puntoPartida, i))
                elif self.trans == ';':
                    self.tokens += 1
                    self.estadoActual = self.inicio
                    self.tokensEncontrados += [[self.nombreID(self.puntoPartida, i), "Flotante", "Número"]]
                    self.tokensEncontrados += [[self.trans, "Finaliza una línea/instrucción", "Carácter"]]
                    print("Se encontró al número flotante: %s" % self.nombreID(self.puntoPartida, i).replace(";", ""))
                    print("Se encontró el fin de una instrucción: %s" % self.trans)
                elif self.trans == ' ':
                    self.tokens += 1
                    self.tokensEncontrados += [[self.nombreID(self.puntoPartida, i), "Flotante", "Número"]]
                    print("Se encontró al número flotante: %s" % self.nombreID(self.puntoPartida, i))
                    self.estadoActual = self.inicio
                else:
                    self.estadoActual = self.inicio
            
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
                    self.imprimirError1("ifndef")
            elif self.estadoActual == 'GN1':
                if self.trans == 'c':
                    self.estadoActual = 'GN2'
                else:
                    self.imprimirError1("include")
            elif self.estadoActual == 'GN2':
                if self.trans == 'l':
                    self.estadoActual = 'GN3'
                else:
                    self.imprimirError1("include")
            elif self.estadoActual == 'GN3':
                if self.trans == 'u':
                    self.estadoActual = 'GN4'
                else:
                    self.imprimirError1("include")
            elif self.estadoActual == 'GN4':
                if self.trans == 'd':
                    self.estadoActual = 'GN5'
                else:
                    self.imprimirError1("include")
            elif self.estadoActual == 'GN5':
                if self.trans == 'e':
                    self.tokens += 1
                    self.estadoActual = self.inicio
                    self.tokensEncontrados += [["#include", "Directiva", "Carácter"]]
                    print("Se encontró la directiva #include")
                else:
                    self.imprimirError1("include")
            elif self.estadoActual == 'GF1':
                if self.trans == 'n':
                    self.estadoActual = 'GF2'
                else:
                    self.imprimirError1("ifndef")
            elif self.estadoActual == 'GF2':
                if self.trans == 'd':
                    self.estadoActual = 'GF3'
                else:
                    self.imprimirError1("ifndef")
            elif self.estadoActual == 'GF3':
                if self.trans == 'e':
                    self.estadoActual = 'GF4'
                else:
                    self.imprimirError1("ifndef")
            elif self.estadoActual == 'GF4':
                if self.trans == 'f':
                    self.tokens += 1
                    self.estadoActual = self.inicio
                    self.tokensEncontrados += [["#ifndef", "Directiva", "Carácter"]]
                    print("Se encontró la directiva #ifndef")
                else:
                    self.imprimirError1("ifndef")

            elif self.estadoActual == 'GD1':
                if self.trans == 'e':
                    self.estadoActual = 'GD2'
                else:
                    self.imprimirError1("define")
            elif self.estadoActual == 'GD2':
                if self.trans == 'f':
                    self.estadoActual = 'GD3'
                else:
                    self.imprimirError1("define")
            elif self.estadoActual == 'GD3':
                if self.trans == 'i':
                    self.estadoActual = 'GD4'
                else:
                    self.imprimirError1("define")
            elif self.estadoActual == 'GD4':
                if self.trans == 'n':
                    self.estadoActual = 'GD5'
                else:
                    self.imprimirError1("define")
            elif self.estadoActual == 'GD5':
                if self.trans == 'e':
                    self.tokens += 1
                    self.estadoActual = self.inicio
                    self.tokensEncontrados += [["#define", "Directiva", "Carácter"]]
                    print("Se encontró la directiva #define")
                else:
                    self.imprimirError1("define")

            elif self.estadoActual == 'GE1':
                if self.trans == 'n':
                    self.estadoActual = 'GE2'
                else:
                    self.imprimirError1("endif")
            elif self.estadoActual == 'GE2':
                if self.trans == 'd':
                    self.estadoActual = 'GE3'
                else:
                    self.imprimirError1("endif")
            elif self.estadoActual == 'GE3':
                if self.trans == 'i':
                    self.estadoActual = 'GE4'
                else:
                    self.imprimirError1("endif")
            elif self.estadoActual == 'GE4':
                if self.trans == 'f':
                    self.tokens += 1
                    self.estadoActual == self.inicio
                    self.tokensEncontrados += [["endif", "Directiva", "Carácter"]]
                    print("Se encontró la directiva #endif")
                else:
                    self.imprimirError1("endif")

            elif self.estadoActual == 'PP':
                self.puntoPartida = i
                if self.trans.isdigit():
                    self.estadoActual = 'D'
                elif not self.trans.isdigit() and self.trans.isalnum():
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
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Inicio de agrupación", "Agrupación"]]
                        print("Se encontró un inicio de agrupación: %s" % self.trans)
                        self.estadoActual = 'PP'
                    elif self.trans == '{':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Inicio de statement", "Agrupación"]]
                        print("Se encontró un inicio de apertura de statements: %s" % self.trans)
                        self.estadoActual = 'AS'
                    elif self.trans == '<':
                        self.estadoActual = 'MQ'
                    elif self.trans == '>':
                        self.estadoActual = 'MYQ'
                    elif self.trans == '\"':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Inicio de string (comillas dobles)", "String"]]
                        print("Se encontró la apertura de un string con comillas dobles: %s" % self.trans)
                        self.estadoActual = 'STRR'
                    elif self.trans == ',':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Separa variables", "Carácter"]]
                        print("Se encontró el separador de variables: %s" % self.trans)
                        self.estadoActual = self.inicio
                    elif self.trans == '\'':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Inicio de string (comillas simples)", "String"]]
                        print("Se encontró el inicio de un string con comillas simples: %s" % self.trans)
                        self.estadoActual = 'STR'
                    elif self.trans == ')':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Fin de una agrupación", "Agrupación"]]
                        print("Se encontró el fin de una agrupación: %s" % self.trans)
                        self.estadoActual = self.inicio
                    elif self.trans == ':':
                        self.estadoActual = 'DP'
                    elif self.trans == '.':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Llama a métodos", "---"]]
                        self.estadoActual = self.inicio
                        print("Se ha encontrado el símbolo para añadir métodos: %s" % self.trans)
                    elif self.trans == '}':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Finaliza un statement", "Agrupación"]]
                        print("Se encontró el fin de un statement: %s" % self.trans)
                        self.estadoActual = self.inicio
                    elif self.trans == '=':
                        self.estadoActual = 'OA'
                    elif self.trans == ';':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Finaliza una línea/instrucción", "Carácter"]]
                        print("Se encontró el fin de una instrucción: %s" % self.trans)
                        self.estadoActual = self.inicio
                    elif self.trans == '+':
                        self.estadoActual = 'ACUM'
                    elif self.trans == '-':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Resta", "Operador"]]
                        print("Se encontró el operador de resta: %s" % self.trans)
                        self.estadoActual = self.inicio
                    elif self.trans == '*':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Multiplicación", "Operador"]]
                        print("Se encontró el operador de multiplicación: %s" % self.trans)
                        self.estadoActual = self.inicio
                    elif self.trans == '/':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "División", "Operador"]]
                        print("Se encontró el operador de división: %s" % self.trans)
                        self.estadoActual = self.inicio
                    elif self.trans == '\n':
                        self.linea += 1
                    elif self.trans == ' ' or self.trans == '\t':
                        pass
                    else:
                        quit("Error: símbolo desconocido: '%s', en la línea %d" % (self.trans, self.linea))

            elif self.estadoActual == 'AS':
                self.puntoPartida = i
                if self.trans.isdigit():
                    self.estadoActual = 'D'
                elif not self.trans.isdigit() and self.trans.isalnum():
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
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Inicio de agrupación", "Agrupación"]]
                        print("Se encontró un inicio de agrupación: %s" % self.trans)
                        self.estadoActual = 'PP'
                    elif self.trans == '{':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Inicio de statement", "Agrupación"]]
                        print("Se encontró un inicio de apertura de statements: %s" % self.trans)
                        self.estadoActual = 'AS'
                    elif self.trans == '<':
                        self.estadoActual = 'MQ'
                    elif self.trans == '>':
                        self.estadoActual = 'MYQ'
                    elif self.trans == '\"':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Inicio de string (comillas dobles)", "String"]]
                        print("Se encontró la apertura de un string con comillas dobles: %s" % self.trans)
                        self.estadoActual = 'STRR'
                    elif self.trans == ',':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Separa variables", "Carácter"]]
                        print("Se encontró el separador de variables: %s" % self.trans)
                        self.estadoActual = self.inicio
                    elif self.trans == '\'':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Inicio de string (comillas simples)", "String"]]
                        print("Se encontró el inicio de un string con comillas simples: %s" % self.trans)
                        self.estadoActual = 'STR'
                    elif self.trans == ')':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Fin de una agrupación", "Agrupación"]]
                        print("Se encontró el fin de una agrupación: %s" % self.trans)
                        self.estadoActual = self.inicio
                    elif self.trans == ':':
                        self.estadoActual = 'DP'
                    elif self.trans == '.':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Llama a métodos", "---"]]
                        self.estadoActual = self.inicio
                        print("Se ha encontrado el símbolo para añadir métodos: %s" % self.trans)
                    elif self.trans == '}':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Finaliza un statement", "Agrupación"]]
                        print("Se encontró el fin de un statement: %s" % self.trans)
                        self.estadoActual = self.inicio
                    elif self.trans == '=':
                        self.estadoActual = 'OA'
                    elif self.trans == ';':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Finaliza una línea/instrucción", "Carácter"]]
                        print("Se encontró el fin de una instrucción: %s" % self.trans)
                        self.estadoActual = self.inicio
                    elif self.trans == '+':
                        self.estadoActual = 'ACUM'
                    elif self.trans == '-':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Resta", "Operador"]]
                        print("Se encontró el operador de resta: %s" % self.trans)
                        self.estadoActual = self.inicio
                    elif self.trans == '*':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "Multiplicación", "Operador"]]
                        print("Se encontró el operador de multiplicación: %s" % self.trans)
                        self.estadoActual = self.inicio
                    elif self.trans == '/':
                        self.tokens += 1
                        self.tokensEncontrados += [[self.trans, "División", "Operador"]]
                        print("Se encontró el operador de división: %s" % self.trans)
                        self.estadoActual = self.inicio
                    elif self.trans == '\n':
                        self.linea += 1
                    elif self.trans == ' ' or self.trans == '\t':
                        pass
                    else:
                        quit("Error: símbolo desconocido. '%s', en la línea %d" % (self.trans, self.linea))

            elif self.estadoActual == 'OA':
                if self.trans == '=':
                    self.tokens += 1
                    self.tokensEncontrados += [["==", "Comparación", "Operador"]]
                    print("Se encontró el operador de comparación: =%s" % self.trans)
                    self.estadoActual = self.inicio
                else:
                    self.tokens += 1
                    self.tokensEncontrados += [["=", "Asignación", "Operador"]]
                    print("Se encontró el operador de asignación: %s" % self.contenidoArchivo[i - 1])
                    self.estadoActual = self.inicio

            elif self.estadoActual == 'ACUM':
                if self.trans == '=':
                    self.tokens += 1
                    self.tokensEncontrados += [["+=", "Acumulación", "Operador"]]
                    print("Se ha encontrado el operador de acumulación: +%s" % self.trans)
                    self.estadoActual = self.inicio
                else:
                    self.tokens += 1
                    self.tokensEncontrados += [["+", "Suma", "Operador"]]
                    print("Se encontró el operador de suma: %s" % self.contenidoArchivo[i - 1])
                    self.estadoActual = self.inicio

            #identificación de string con comillas dobles
            elif self.estadoActual == 'STRR':
                if self.trans == '\"':
                    self.tokens += 1
                    self.tokensEncontrados += [["\"", "Finaliza un string (comillas dobles)", "String"]]
                    print("Se ha reconocido el fin de un string de comillas dobles: %s" % self.contenidoArchivo[i - 1])
                    self.estadoActual = self.inicio
                elif self.trans == '\n':
                    quit("Error, comillas no cerradas: %s en la línea %d" % (self.trans, self.linea))
                else:
                    self.estadoActual = 'STRR'

            #identificación de string con comillas simples
            elif self.estadoActual == 'STR':
                if self.trans == '\'':
                    self.tokens += 1 
                    self.tokensEncontrados += [["\'", "Finaliza un string (comillas simples)", "String"]]
                    print("Se ha reconocido el fin de un string de comillas simples: %s" % self.trans)
                    self.estadoActual = self.inicio
                elif self.trans == '\n':
                    quit("Error, comillas no cerradas: %s en la línea %d" % (self.contenidoArchivo[i - 1], self.linea))
                else:
                    self.estadoActual = 'STR'

            elif self.estadoActual == 'MQ':
                if self.trans == '<':
                    self.tokens += 1
                    self.tokensEncontrados += [["<<", "Muestra texto", "Operador"]]
                    print("Se encontró el operador de salida de texto: %s%s" % (self.trans, self.contenidoArchivo[i - 1]))
                    self.estadoActual = self.inicio
                elif self.trans == '=':
                    self.tokens += 1
                    self.tokensEncontrados += [["<=", "Comparación (menor o igual que)", "Operador"]]
                    print("Se ha encontrado al operador de comparación 'menor o igual que': %s%s" % (self.contenidoArchivo[i - 1], self.trans))
                    self.estadoActual = self.inicio
                elif self.trans.isdigit():
                    self.puntoPartida = i
                    self.estadoActual = 'D'
                elif not self.trans.isdigit():
                    self.tokens += 1
                    self.tokensEncontrados += [["<", "Inclusión de librería", "Carácter"]]
                    print("Se encontró el carácter para incluir librería: %s" % self.contenidoArchivo[i - 1])
                    self.estadoActual = self.inicio
                else:
                    self.tokens += 1
                    self.tokensEncontrados += [["<", "Comparación (menor que)", "Operador"]]
                    print("Se encontró el operador de comparación 'menor que': %s" % self.contenidoArchivo[i - 1])
                    self.estadoActual = self.inicio

            elif self.estadoActual == 'MYQ':
                if self.trans == '=':
                    self.tokens += 1
                    self.tokensEncontrados += [[">=", "Comparación (mayor o igual que)", "Operador"]]
                    print("Se ha encontrado el operador de comparación 'mayor o igual que': %s%s" % (self.contenidoArchivo[i - 1], self.trans))
                    self.estadoActual = self.inicio
                else:
                    if self.contenidoArchivo[i - 1].isdigit():
                        self.tokens += 1
                        self.tokensEncontrados += [[">", "Comparación (mayor que)", "Operador"]]
                        print("Se ha encontrado el operador de comparación 'mayor que': %s" % self.contenidoArchivo[i - 1])
                        self.estadoActual = self.inicio
                    else:
                        self.tokens += 1
                        self.tokensEncontrados += [[">", "Cierra la inclusión de una librería", "Carácter"]]
                        print("Se ha encontrado el símbolo para cerrar inclusión de librería: %s" % self.contenidoArchivo[i - 1])
                        self.estadoActual = self.inicio

            elif self.estadoActual == 'DP':
                if self.trans == ':':
                    self.tokens += 1
                    self.estadoActual = self.inicio
                    self.tokensEncontrados += [["::", "Resolución de alcance", "Operador"]]
                    print("Se ha encontrado el operador de resolución de alcance: %s%s" % (self.contenidoArchivo[i - 1], self.trans))
                else:
                    self.tokens += 1
                    self.estadoActual = self.inicio
                    self.tokensEncontrados += [[":", "Definición de funciones", "Operador"]]
                    print("Se ha encontrado el símbolo para definicr funciones: %s" % self.contenidoArchivo[i - 1])

            elif self.estadoActual == 'FIN':
                self.estadoActual = self.inicio
            

        print(self.valoresEncontrados)
        print("-"*40)
        print("Tokens encontrados: %d" % self.tokens)
        print("Número de líneas del código: %d" % self.linea)
        print("*"*80)
        
        return self.tokensEncontrados
        

    def imprimirError1(self, dir):
        quit("Error: definición de directiva no pertenece al léxico: '%s' en la línea %d" % (dir, self.linea))

    # def buscarError(self, tok):
    #     errL = 0

    #     f = open(self.nombreArchivo, "r")
    #     for line in f:
    #         errL += 1

                        
    def nombreID(self, inicio, fin):
        arregloID = []
        self.var = ''
        for i in range(inicio, fin):
            arregloID.append(self.contenidoArchivo[i])
        return "".join(arregloID)
        

# analizador = (Analizador()).leerEntrada().automata()
# print("\t\t\tTabla de tokens")
# print("  TOKEN \t    DESCRIPCIÓN \t\t TIPO")
# print(tabulate(analizador))
