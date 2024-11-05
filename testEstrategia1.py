import numpy as np
import time
from pyemd import emd # EMD

class Estrategia1:
    def estrategia_recursiva(self, V, matrices, full_dist, background_indices):
        """
        Algoritmo iterativo-recursivo para encontrar la mejor partición minimizando EMD.
        """
        if len(V) <= 2:
            return V  # Caso base: Dos nodos restantes

        W1 = {V[0]}  # Inicia con un elemento arbitrario
        V_restante = set(V) - W1  # Elementos restantes
        pares_candidatos = []

        # Función para calcular la EMD de un subconjunto
        def calcular_emd(subset):
            subset_dist = self.marginalizar_distribution(matrices, list(subset), background_indices)
            return wasserstein_distance(full_dist, subset_dist)

        # Iteración principal: Seleccionar el elemento que minimice la EMD
        for vi in V_restante:
            emd_value = calcular_emd(W1 | {vi}) - calcular_emd({vi})
            pares_candidatos.append((vi, emd_value))

        # Seleccionar el mejor elemento para añadir a W1
        mejor_vi = min(pares_candidatos, key=lambda x: x[1])[0]
        W1.add(mejor_vi)

        # Recursión: Reemplazar los dos últimos nodos por un nodo virtual
        if len(W1) > 2:
            nodo_virtual = max(V) + 1  # Crear nodo virtual
            V_actualizado = (V_restante - {mejor_vi}) | {nodo_virtual}
            return self.estrategia_recursiva(V_actualizado, matrices, full_dist, background_indices)

        return W1

    def marginalizar_distribution(self, matriz, subset, background_indices):
        """
        Elimina los nodos de background y suma sus probabilidades a los estados correspondientes.
        """
        matriz_reducida = np.delete(np.delete(matriz, background_indices, axis=0), background_indices, axis=1)
        prob_acumulada = np.sum(matriz[background_indices, :], axis=0)
        matriz_reducida += prob_acumulada  # Ajuste de probabilidades
        return np.sum(matriz_reducida[subset, :], axis=0)

    def ejecutar_estrategia(self, opcion):
        """
        Ejecuta la estrategia recursiva utilizando los datos cargados y mide el tiempo de ejecución.
        """
        matrices = LogicaPB.datosMatrices(self, opcion)
        estados_actuales = LogicaPB.retornarEstados(self, matrices)
        estados_futuros = LogicaPB.retornarEstadosFuturos(self, matrices)

        # Inicialización de los conjuntos
        V = list(range(len(estados_actuales)))
        background_indices = [estados_actuales.index(e) for e in estados_actuales if "'" in e]
        full_dist = np.sum(matrices, axis=0)  # Distribución total

        # Medición del tiempo de ejecución
        inicio = time.time()
        mejor_particion = self.estrategia_recursiva(V, matrices, full_dist, background_indices)
        fin = time.time()

        tiempo_ejecucion = fin - inicio
        return mejor_particion, tiempo_ejecucion
