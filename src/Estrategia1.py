import math
import random
import time
import numpy as np
import pandas as pd
from src.LogicaPB import LogicaPB
from src.condiciones import condiciones
from numpy.typing import NDArray
from pyemd import emd


class Estrategia1:

    def marginalizacion(self):
        print("Marginalización")

    def retornarMatrizCondicionada(self, matrices, c1, estadoActual, candidato):
        """
        Condiciona una matriz y calcula las probabilidades finales basadas en las condiciones dadas.

        Args:
            matrices (list): Lista de matrices a ser condicionadas.
            c1 (any): Condición específica para el proceso de condicionamiento.
            estadoActual (any): Estado actual del sistema.
            candidato (any): Candidato a ser evaluado en el proceso.

        Returns:
            list: Lista de probabilidades finales después de aplicar las condiciones.
        """
        c = condiciones()
        print(matrices)
        matrices_condicionadas = c.condiciona_matriz(
            matrices, estadoActual, candidato, c1)
        probabilidades_finales = c.calcula_probabilidades(
            matrices_condicionadas, estadoActual, candidato, c1)
        return probabilidades_finales

    def distribucion_candidatos(self, c1, c2, valor_actual, candidato, opcion):
        """
        Genera una distribución de probabilidades basada en los candidatos y el valor actual.
        Args:
            c1 (list): Lista de estados actuales.
            c2 (list): Lista de estados futuros.
            valor_actual (int/float): Valor actual del estado.
            candidato (int/float): Valor del candidato.
            opcion (int): Opción seleccionada para obtener las matrices de datos.
        Returns:
            pd.DataFrame: DataFrame con la distribución de probabilidades generada.
        """
        matrices = LogicaPB.datosMatrices(self, opcion)
        matricesP = Estrategia1.retornarMatrizCondicionada(
            self, matrices, c1, valor_actual, candidato)
        c1 = LogicaPB.retornarEstados(self, matricesP)
        c2 = LogicaPB.retornarEstadosFuturos(self, matricesP)
        resultado, estados = LogicaPB.generarEstadoTransicion(self, matricesP)
        datos = LogicaPB.generarDistribucionProbabilidades(
            self, matricesP, c1, c2, valor_actual, estados)
        lista = []
        lista.append(str(datos[0][0]))

        # lista.append(datos[0])
        for i in range(len(datos[0][1:])):
            lista.append(str(datos[0][1:][i]))

        df = pd.DataFrame(datos[1:], columns=lista)
        return df

    def retornarMejorParticion(self, c1, c2, estadoActual, candidato, opcion):
        matrices = LogicaPB.datosMatrices(self, opcion)
        matricesP = Estrategia1.retornarMatrizCondicionada(
            self, matrices, c1, estadoActual, candidato)
        c1 = self.retornarEstados(self, matricesP)
        c2 = self.retornarEstadosFuturos(self, matricesP)
        resultado, estados = LogicaPB.generarEstadoTransicion(self, matricesP)
        distribucionProbabilidadOriginal = LogicaPB.generarDistribucionProbabilidades(
            self, matricesP, c1, c2, estadoActual, estados)
        lista = []
        particion, diferencia, tiempo, lista = Estrategia1.busqueda_voraz(
            self, matricesP, estados, distribucionProbabilidadOriginal, c1, c2, estadoActual)
        return particion, diferencia, tiempo, lista

    def retornar_mejor_particion(self, c1, c2, estadoActual, candidato, opcion):
        matrices = LogicaPB.datosMatrices(self, opcion)
        matricesP = Estrategia1.retornarMatrizCondicionada(
            self, matrices, c1, estadoActual, candidato)
        c1 = LogicaPB.retornarEstados(self, matricesP)
        c2 = LogicaPB.retornarEstadosFuturos(self, matricesP)
        resultado, estados = LogicaPB.generarEstadoTransicion(
            self, matricesP)
        distribucionProbabilidadOriginal = LogicaPB.generarDistribucionProbabilidades(
            self, matrices, c1, c2, estadoActual, estados)
        lista = []
        inicio = time.time()
        particion, diferencia, tiempo, lista = Estrategia1.busqueda_voraz(
            self, matrices, estados, distribucionProbabilidadOriginal, c1, c2, estadoActual)
        fin = time.time()
        tiempoEjecucion = fin - inicio

        return particion, diferencia, tiempoEjecucion, lista

    def obtener_diferencia(self, c1_izq, c2_izq, c1_der, c2_der, matrices, estadoActual, disOriginal, estados):
        distribucion_izq = LogicaPB.generarDistribucionProbabilidades(
            self, matrices, c1_izq, c2_izq, estadoActual, estados)
        distribucion_der = LogicaPB.generarDistribucionProbabilidades(
            self, matrices, c1_der, c2_der, estadoActual, estados)
        p1 = distribucion_izq[1][1:]
        p2 = distribucion_der[1][1:]
        prodTensor = Estrategia1.producto_tensor(self, p1, p2)
        diferencia = Estrategia1.calcularEMD(
            self, disOriginal[1][1:], prodTensor)
        return diferencia

    def generar_vecino(self, c1, c2):
        mitad_c1 = len(c1) // 2
        mitad_c2 = len(c2) // 2
        c1_izq = random.sample(c1, mitad_c1)
        c1_der = list(set(c1) - set(c1_izq))
        c2_izq = random.sample(c2, mitad_c2)
        c2_der = list(set(c2) - set(c2_izq))
        return c1_izq, c2_izq, c1_der, c2_der

    def pintarGrafoGenerado(self, c1, c2, estadoActual, nodes, edges, st, opcion, factor):
        particion, diferencia, tiempo, lista = Estrategia1.retornar_mejor_particion(
            self, c1, c2, estadoActual, opcion, factor)
        p1, p2 = particion
        for i in p1[1]:
            if i not in p2[1]:
                for arista in edges:
                    if arista.source == i and arista.to in p2[0]:
                        arista.dashes = True
                        arista.color = 'rgba(254, 20, 56, 0.5)'
        for i in p2[1]:
            if i not in p1[1]:
                for arista in edges:
                    if arista.source == i and arista.to in p1[0]:
                        arista.dashes = True
                        arista.color = 'rgba(254, 20, 56, 0.5)'

        st.write('Partición: ', str(particion))
        st.write('Perdida: ', diferencia)
        st.write('Tiempo: ', tiempo)

    def calcularEMD(self, p1: list[float], p2: list[float]) -> float:
        """
        Calcula la Earth Mover's Distance (EMD) entre dos listas de valores.
        La matriz de costos se genera utilizando la distancia de Hamming.
        """

        # Convertir listas a arrays de NumPy
        p1_array: NDArray[np.float64] = np.array(p1, dtype=np.float64)
        p2_array: NDArray[np.float64] = np.array(p2, dtype=np.float64)

        # Asegurar que ambos vectores sean unidimensionales
        if p1_array.ndim != 1 or p2_array.ndim != 1:
            raise ValueError("Ambos vectores deben ser unidimensionales.")

        # Interpolación si las longitudes son diferentes
        if len(p1_array) != len(p2_array):
            p2_array = np.interp(np.linspace(0, 1, len(p1_array)),
                                 np.linspace(0, 1, len(p2_array)), p2_array)

        # Crear la matriz de costos usando la distancia de Hamming
        n: int = len(p1_array)
        cost_matrix: NDArray[np.float64] = np.empty((n, n), dtype=np.float64)

        for i in range(n):
            for j in range(n):
                cost_matrix[i, j] = Estrategia1.hamming_distance(i, j)

        # Calcular y retornar EMD
        return emd(p1_array, p2_array, cost_matrix)

   

    def hamming_distance(a: int, b: int):
        return (a ^ b).bit_count()

    def producto_tensor(self, p1, p2):
        """
        Computes the tensor product of two input arrays and returns the result as a flattened array.

        Parameters:
        p1 (array-like): The first input array.
        p2 (array-like): The second input array.

        Returns:
        numpy.ndarray: A flattened array representing the tensor product of the input arrays.
        """
        p1 = np.array(p1)
        p2 = np.array(p2)
        return np.outer(p1, p2).flatten()

    def retornarMejorParticionE1(self, c1, c2, estadoActual, opcion):
        matrices = LogicaPB.datosMatrices(self, opcion)
        resultado, estados = LogicaPB.generarEstadoTransicion(self, matrices)
        distribucionProbabilidadOriginal = LogicaPB.generarDistribucionProbabilidades(
            self, matrices, c1, c2, estadoActual, estados)
        lista = []
        inicio = time.time()
        particion, diferencia, tiempo, lista = Estrategia1.busqueda_voraz(
            self, matrices, estados, distribucionProbabilidadOriginal, c1, c2, estadoActual)
        fin = time.time()
        tiempoEjecucion = fin - inicio
        return particion, diferencia, tiempoEjecucion, lista

    def busqueda_voraz(self, matrices, estados, distribucionProbabilidadOriginal, c1, c2, estadoActual):
        """
        Realiza una búsqueda voraz para encontrar la mejor partición de los conjuntos c1 y c2 que minimice la diferencia
        entre la distribución de probabilidad original y el producto tensorial de las distribuciones resultantes de las particiones.
        Args:
            matrices (list): Lista de matrices utilizadas en la estrategia.
            estados (list): Lista de estados posibles.
            distribucionProbabilidadOriginal (list): Distribución de probabilidad original.
            c1 (list): Primer conjunto de elementos a particionar.
            c2 (list): Segundo conjunto de elementos a particionar.
            estadoActual (int): Estado actual del sistema.
        Returns:
            tuple: Una tupla que contiene:
            - mejor_particion (list): La mejor partición encontrada que minimiza la diferencia.
            - menor_diferencia (float): La menor diferencia encontrada entre la distribución original y el producto tensorial.
            - int: Un valor fijo (0) que puede ser utilizado para otros propósitos.
            - listaParticionesEvaluadas (list): Lista de todas las particiones evaluadas junto con sus diferencias.
        """
        mejor_particion = []
        menor_diferencia = float('inf')
        listaParticionesEvaluadas = []

        for i in range(len(c1)):

            c1_izq = c1[:i]
            c1_der = c1[i:]
            c2_izq = []
            c2_der = list(c2)

            for j in range(len(c2)):
                c2_izq.append(c2_der.pop(0))

                distribucion_izq = Estrategia1.estrategiaUno(
                    self, matrices, c1_izq, c2_izq, estadoActual, estados)
                distribucion_der = Estrategia1.estrategiaUno(
                    self, matrices, c1_der, c2_der, estadoActual, estados)
                p1 = distribucion_izq[1][1:]
                p2 = distribucion_der[1][1:]
                prodTensor = Estrategia1.producto_tensor(self, p1, p2)
                diferencia = Estrategia1.calcularEMD(
                    self, distribucionProbabilidadOriginal[1][1:], prodTensor)

                aux = []
                if c2_der == [] and c1_der == []:
                    continue
                elif diferencia < menor_diferencia:
                    menor_diferencia = diferencia
                    mejor_particion = [
                        (tuple(c2_izq), (tuple(c1_izq))), (tuple(c2_der), tuple(c1_der))]
                aux = [(tuple(c2_izq), (tuple(c1_izq))),
                       (tuple(c2_der), tuple(c1_der)), str(diferencia)]
                listaParticionesEvaluadas.append(aux)

        return mejor_particion, menor_diferencia, 0, listaParticionesEvaluadas

    def estrategiaUno(self, matrices, c1, c2, estadoActual, estados):
        tabla = {}
        # Creamos una llave única para la tabla
        key = (tuple(c1), tuple(c2), estadoActual)
        if key not in tabla:
            tabla[key] = LogicaPB.generarDistribucionProbabilidades(
                self, matrices, c1, c2, estadoActual, estados)
        return tabla[key]
