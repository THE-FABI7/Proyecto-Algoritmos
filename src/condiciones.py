import itertools


class condiciones:

    def condiciona_matriz(self, probabilidades, estado_actual, candidato, c1):
        matriz_condicionada = {}
        for c in candidato:
            matriz_condicionada[c] = {}
            for key in probabilidades[c].keys():
                if all(candidato[i] == key[i] for i in range(len(candidato)) if c1[i] not in candidato):
                    matriz_condicionada[c][key] = probabilidades[c][key]
        return matriz_condicionada

    def calcula_probabilidades(self, matrices_condicionadas, estado_actual, candidato, c1):
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
