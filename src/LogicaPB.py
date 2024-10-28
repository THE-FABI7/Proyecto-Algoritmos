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
        # ocho = datos.retornarDatosMatrizOchoNodos()
        # diez = datos.retornarDatosMatrizDiezNodos()
        salida = None
        if opcion == "Tres Nodos":
            salida = tres
        elif opcion == "Cuatro Nodos":
            salida = cuatro
        elif opcion == "Cinco Nodos":
            salida = cinco
        elif opcion == "Seis Nodos":
            salida = seis
        # elif opcion == "Ocho Nodos":
            # salida = ocho
        # elif opcion == "Diez Nodos":
            # salida = diez
        return salida

    def listaMatrices(self):
        return ["Tres Nodos", "Cuatro Nodos", "Cinco Nodos", "Seis Nodos", "Ocho Nodos", "Diez Nodos"]

    def retornarEstados(self, datos):
        resultado, estados = LogicaPB.generarEstadoTransicion(self, datos)
        return estados

    def generarEstadoTransicion(self, subconjuntos):
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
        lista = [['key', (1,), (0,)]]
        for k, v in diccionario.items():
            lista.append([k, v, 1 - v])
        return lista
