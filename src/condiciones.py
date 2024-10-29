import itertools

import numpy as np


class condiciones:

    def condiciona_matriz(self, probabilidades, estado_actual, candidato, c1):
        """
        Condiciona una matriz de probabilidades basada en un estado actual y un conjunto de candidatos.

        Args:
            probabilidades (dict): Un diccionario donde las claves son los candidatos y los valores son 
                       diccionarios de probabilidades asociadas a cada clave.
            estado_actual (any): El estado actual del sistema (no utilizado en la función).
            candidato (list): Una lista de candidatos a considerar para la matriz condicionada.
            c1 (list): Una lista de condiciones adicionales que se utilizan para filtrar las probabilidades.

        Returns:
            dict: Un diccionario que representa la matriz condicionada, donde las claves son los candidatos 
              y los valores son diccionarios de probabilidades filtradas según las condiciones.
        """
        matriz_condicionada = {}
        for c in candidato:
            matriz_condicionada[c] = {}
            for key in probabilidades[c].keys():
                if all(candidato[i] == key[i] for i in range(len(candidato)) if c1[i] not in candidato):
                    matriz_condicionada[c][key] = probabilidades[c][key]
        return matriz_condicionada

    def calcula_probabilidades(self, matrices_condicionadas, estado_actual, candidato, c1):
        """
        Calcula las probabilidades condicionadas para un conjunto de candidatos dado el estado actual.
        Args:
            matrices_condicionadas (dict): Un diccionario donde las claves son los candidatos y los valores son 
                           matrices de probabilidades condicionadas.
            estado_actual (tuple): El estado actual del sistema representado como una tupla.
            candidato (list): Una lista de candidatos para los cuales se calcularán las probabilidades.
            c1 (list): Una lista que contiene el orden de los candidatos en el estado.
        Returns:
            dict: Un diccionario donde las claves son los candidatos y los valores son diccionarios que contienen 
              las combinaciones de estados futuros y sus probabilidades asociadas.
        """
        probabilidad_total = {}
        combinaciones = list(itertools.product([0, 1], repeat=len(candidato)))

        for c in candidato:
            probabilidad_total[c] = {}
            for combinacion in combinaciones:
                # Crear una clave de estado futuro basada en la combinación actual
                estado_futuro = list(estado_actual)
                for i, val in enumerate(combinacion):
                    idx = c1.index(candidato[i])
                    estado_futuro[idx] = val
                estado_futuro = tuple(estado_futuro)

                # Asignar los valores proporcionados a las combinaciones
                clave_combinacion = tuple(
                    estado_futuro[c1.index(val)] for val in candidato)
                probabilidad_total[c][clave_combinacion[::-1]
                                      ] = matrices_condicionadas[c].get(estado_futuro, 0)

        return probabilidad_total

    def marginalizar_background(self, matriz, background):
        """
        Elimina los nodos de background y suma sus probabilidades a los estados correspondientes.
        """
        # Eliminar filas y columnas del background
        matriz_reducida = np.delete(np.delete(matriz, background, axis=0), background, axis=1)
        
        # Sumar las probabilidades eliminadas a los estados restantes
        prob_acumulada = np.sum(matriz[background, :], axis=0)
        matriz_reducida += prob_acumulada  # Ajuste de probabilidades
        return matriz_reducida