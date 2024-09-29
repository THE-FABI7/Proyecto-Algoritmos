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
        resultado, estados = self.generarEstadoTransicion(datos)
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
        resultado, estados = self.generarEstadoTransicion(datos)
        # agregarle a cada valor de los estados una '
        for i in range(len(estados)):
            estados[i] = estados[i] + "'"
        return estados

    def retornarValorActual(self, c1, c2, opcion):
        lista = []
        matrices = self.datosMatrices(opcion)
        for j in matrices['A']:
            lista.append(j)
        return lista
