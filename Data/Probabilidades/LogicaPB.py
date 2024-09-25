from Data.Probabilidades.Datos import Datos


class LogicaPB:
    
    def datosMatrices(opcion):
        tres = Datos().retornarDatosTresNodos()
        cuatro = Datos().retornarDatosCuatroNodos()
        cinco = Datos().retornarDatosCincoNodos()
        seis = Datos().retornarDatosSeisNodos()
        # ocho = Datos().retornarDatosMatrizOchoNodos()
        # diez = Datos().retornarDatosMatrizDiezNodos()
        salida = None
        if opcion == "Tres Nodos":
            salida = tres
        if opcion == "Cuatro Nodos":
            salida = cuatro
        if opcion == "Cinco Nodos":
            salida =  cinco
        if opcion == "Seis Nodos":
            salida = seis  
        # if opcion == "Ocho Nodos":
            # salida = ocho
        # if opcion == "Diez Nodos":
            # salida = diez
        return salida

    def listaMatrices():
        opcion = ["Tres Nodos", "Cuatro Nodos", "Cinco Nodos",
                  "Seis Nodos", "Ocho Nodos", "Diez Nodos"]
        return opcion
    
    def retornarEstados(datos):
        
        resultado, estados = LogicaPB.generarEstadoTransicion(datos)
        return estados
    
    def generarEstadoTransicion(subconjuntos):
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

    def retornarEstadosFuturos(datos):

        resultado, estados = LogicaPB.generarEstadoTransicion(datos)
        # agregarle a cada valor de los estados una '
        for i in range(len(estados)):
            estados[i] = estados[i] + "'"

        return estados


















































