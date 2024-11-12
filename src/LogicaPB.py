import itertools
from Data.Probabilidades.Datos import Datos


class LogicaPB:

    def datosMatrices(self, opcion):
        # Se accede a los datos usando una instancia de Datos
        datos = Datos()
        tres = datos.retornarDatosTresNodos()
        cuatro = datos.retornarDatosCuatroNodos()
        cinco = datos.retornarDatosCincoNodos()
        seis = datos.retornarDatosSeisNodos()
        ocho = datos.retornarDatosMatrizOchoNodos()
        diez = datos.retornarDatosMatrizDiezNodos()
        quince = datos.retornarQuinceNodos()
        salida = None
        if opcion == "Tres Nodos":
            salida = tres
        elif opcion == "Cuatro Nodos":
            salida = cuatro
        elif opcion == "Cinco Nodos":
            salida = cinco
        elif opcion == "Seis Nodos":
            salida = seis
        elif opcion == "Ocho Nodos":
            salida = ocho
        elif opcion == "Diez Nodos":
            salida = diez
        elif opcion == "Quince Nodos":
            salida = quince
        return salida

    def listaMatrices(self):
        return ["Tres Nodos", "Cuatro Nodos", "Cinco Nodos", "Seis Nodos", "Ocho Nodos", "Diez Nodos", "Quince Nodos"]

    def retornarEstados(self, datos):
        resultado, estados = LogicaPB.generarEstadoTransicion(self, datos)
        return estados

    def generarEstadoTransicion(self, subconjuntos):
        """
        Genera el estado de transición para un conjunto de subconjuntos dados.
        Args:
            subconjuntos (dict): Un diccionario donde las claves son los estados y los valores son 
                                 diccionarios que representan las transiciones de estado.
        Returns:
            tuple: Una tupla que contiene:
                - transiciones (dict): Un diccionario donde las claves son tuplas que representan 
                                       el estado actual y los valores son tuplas que representan 
                                       el estado futuro.
                - estados (list): Una lista de los estados presentes en los subconjuntos.
        """
        print(subconjuntos.keys())
        estados = list(subconjuntos.keys())
        transiciones = {}
        estado_actual = [0] * len(estados)

        def aux(i):
            if i == len(estados):
                estado_actual_tuple = tuple(estado_actual)
                estado_futuro = tuple(
                    subconjuntos[estado][estado_actual_tuple] for estado in estados)
                transiciones[estado_actual_tuple] = estado_futuro
            else:
                estado_actual[i] = 0
                aux(i + 1)
                estado_actual[i] = 1
                aux(i + 1)
        aux(0)
        return transiciones, estados

    def retornarEstadosFuturos(self, datos):
        """
        Genera y retorna una lista de estados futuros basados en los datos proporcionados.

        Args:
            datos (any): Los datos necesarios para generar los estados de transición.

        Returns:
            list: Una lista de estados futuros, cada uno con un apóstrofo añadido al final.
        """
        resultado, estados = LogicaPB.generarEstadoTransicion(self, datos)
        # agregarle a cada valor de los estados una '
        for i in range(len(estados)):
            estados[i] = estados[i] + "'"
        return estados

    def retornarValorActual(self, c1, c2, opcion):
        lista = []
        matrices = LogicaPB.datosMatrices(self, opcion)
        for j in matrices['A']:
            lista.append(j)
        return lista

    def generarDistribucionProbabilidades(self, tabla, estadoActual, estadoFuturo, num, estados):
        """
        Genera una distribución de probabilidades basada en el estado actual y futuro.
        Args:
            tabla (list): La tabla de datos inicial.
            estadoActual (list): Lista de estados actuales.
            estadoFuturo (list): Lista de estados futuros.
            num (int): Un número utilizado para el cálculo de distribución.
            estados (list): Lista de todos los estados posibles.
        Returns:
            list: Una nueva tabla con la distribución de probabilidades generada.
        Raises:
            ValueError: Si algún estado actual no se encuentra en la lista de estados.
        """
        # indice = [estados.index(i) for i in estadoActual]
        try:
            indice = [estados.index(i) for i in estadoActual]
        except ValueError as e:
            print(f"Error: {e}")
            print("estadoActual:", estadoActual)
            print("estados:", estados)
            raise

        probabilidadesDistribuidas = []
        for i in estadoFuturo:
            # verificar si i tiene "'", si es así, se elimina la comilla
            if "'" in i:
                i = i[:-1]
            nuevaTabla = LogicaPB.generarTablaComparativa(self, tabla[i])
            filtro2 = LogicaPB.porcentajeDistribucion(
                self, nuevaTabla, indice, num)
            probabilidadesDistribuidas.append(filtro2)
        tabla = LogicaPB.generarTabla(self, probabilidadesDistribuidas, num)
        tabla[0] = [[estadoFuturo, estadoActual]] + tabla[0]
        tabla[1] = [num] + tabla[1]
        return tabla

    def generarTabla(self, distribucion, num, i=0, numBinario='', nuevoValor=1):
        """
        Genera una tabla de valores binarios y sus correspondientes valores calculados 
        a partir de una distribución dada.

        Args:
            distribucion (list): Una lista de tuplas donde cada tupla contiene información 
                     relevante para la generación de la tabla.
            num (int): Un número que puede ser utilizado en el cálculo (no se utiliza en el código actual).
            i (int, optional): El índice actual en la distribución. Por defecto es 0.
            numBinario (str, optional): La representación binaria actual en forma de cadena. Por defecto es ''.
            nuevoValor (int, optional): El valor calculado actual. Por defecto es 1.

        Returns:
            list: Una lista de dos listas:
              - La primera lista contiene tuplas de valores binarios generados.
              - La segunda lista contiene los valores calculados correspondientes a cada tupla binaria.
        """
        if i == len(distribucion):
            numBinario = '0' * (len(distribucion)-len(numBinario)) + numBinario
            nuevoDato = tuple(int(bit) for bit in numBinario)
            return [[nuevoDato], [nuevoValor]]
        else:
            tabla = LogicaPB.generarTabla(self,
                                          distribucion, num, i+1, numBinario+'0', nuevoValor*distribucion[i][1][2])
            tabla2 = LogicaPB.generarTabla(self,
                                           distribucion, num, i+1, numBinario+'1', nuevoValor*distribucion[i][1][1])
            return [tabla[0]+tabla2[0], tabla[1]+tabla2[1]]

    def porcentajeDistribucion(self, tabla, indice, num):
        """
        Calcula la distribución porcentual de valores en una tabla basada en un índice y un número dado.
        Args:
            tabla (list): Una lista de listas que representa la tabla de datos.
            indice (list): Una lista de índices que se utilizarán para comparar con los elementos de la tabla.
            num (list): Una lista de números que se utilizarán para comparar con los elementos de la tabla.
        Returns:
            list: Una nueva tabla con la distribución porcentual calculada.
        Raises:
            IndexError: Si se produce un error de índice durante la comparación de elementos.
        """
        tablaNueva = [tabla[0]]
        fila = None
        try:
            tabla1 = [fila for fila in tabla[1:] if all(i < len(num) and pos < len(
                fila[0]) and fila[0][pos] == num[i] for i, pos in enumerate(indice))]
        except IndexError as e:
            print(f"IndexError: {e}")
            raise

        nuevosValores = [0, 0]
        for i in tabla1:
            nuevosValores[0] += i[1]
            nuevosValores[1] += i[2]

        total = sum(nuevosValores)
        nuevosValores = [v / total if total != 0 else v for v in nuevosValores]
        nuevaFila = [num, *nuevosValores]
        tablaNueva.append(nuevaFila)
        return tablaNueva

    def generarTablaComparativa(self, diccionario):
        """
        Genera una tabla comparativa a partir de un diccionario dado.

        Args:
            diccionario (dict): Un diccionario donde las claves son los elementos a comparar y los valores son números.

        Returns:
            list: Una lista de listas, donde cada sublista contiene una clave del diccionario, su valor asociado, 
              y la diferencia entre 1 y el valor asociado.
        """
        lista = [['key', (1,), (0,)]]
        for k, v in diccionario.items():
            lista.append([k, v, 1 - v])
        return lista
