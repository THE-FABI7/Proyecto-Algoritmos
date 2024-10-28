import random
import networkx as nx
from src.Estrategia1 import Estrategia1
from src.LogicaPB import LogicaPB
from src.condiciones import condiciones
from streamlit_agraph import agraph, Node, Edge, Config
import streamlit_agraph as stag


class Gui:

    def generar_grafoBipartito(self, nodosG1, nodosG2, Node, Edge):
        # Crear un grafo bipartito
        G = nx.Graph()
        G.add_nodes_from(nodosG1, bipartite=0)
        G.add_nodes_from(nodosG2, bipartite=1)
        G.add_edges_from([(n1, n2) for n1 in nodosG1 for n2 in nodosG2])

        # Agregar pesos a las aristas
        for u, v in G.edges():
            G.edges[u, v]['weight'] = random.randint(1, 1000)

        # Definir las posiciones de los nodos en dos columnas verticales
        pos = {}
        espacio_vertical = 1000 / (max(len(nodosG1), len(nodosG2)) + 1)
        for i, nodo in enumerate(nodosG1, start=1):
            pos[nodo] = [500, i * espacio_vertical]  # Columna izquierda
        for i, nodo in enumerate(nodosG2, start=1):
            pos[nodo] = [900, i * espacio_vertical]  # Columna derecha

        # Crear una lista de nodos con las nuevas coordenadas
        nodes = [Node(id=str(nodo),
                      label=str(nodo),
                      shape=None,
                      x=pos[nodo][0],  # Coordenada x asignada
                      y=pos[nodo][1],  # Coordenada y asignada
                      color='red' if nodo in nodosG1 else 'yellow')  # Color de nodo
                 for nodo in G.nodes()]

        # Crear una lista de aristas
        edges = [Edge(source=str(u), target=str(v), label=str(G.edges[u, v]['weight']), weight=G.edges[u, v]['weight'], type="CURVE_SMOOTH", width=3, directed=True)
                 for u, v in G.edges()]

        # Configuración de la visualización del grafo
        config = Config(height=600, width=800, directed=False,
                        nodeHighlightBehavior=True, highlightColor="#F7A7A6", physics=False)

        # Dibujar el grafo
        agraph(nodes=nodes, edges=edges, config=config)
        # Retornar los nodos y aristas
        return nodes, edges

    def pintarGrafoGeneradoE1(self, c1, c2, estadoActual, nodes, edges, opcion):
        mP, a, b, c = Estrategia1.retornarMejorParticionE1(self,
                                                           c1, c2, estadoActual, opcion)
        p1, p2 = mP
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

    def pintarGrafoGenerado(self, c1, c2, estadoActual, edges, candidato, Node, Edge, opcion):

        mP, a, b, c = Estrategia1.retornar_mejor_particion(
            self, c1, c2, estadoActual, candidato, opcion)
        matrices = LogicaPB.datosMatrices(self, opcion)
        matricesP = Estrategia1.retornarMatrizCondicionada(
            self, matrices, c1, estadoActual, candidato)
        c1 = LogicaPB.retornarEstados(self, matricesP)
        c2 = LogicaPB.retornarEstadosFuturos(self, matricesP)
        nodes, edges = Gui().generar_grafoBipartito(c1, c2, Node, Edge)
        p1, p2 = mP
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

            config = Config(
                width='100%',
                height=700,
                directed=True,
                physics=False,
                nodeHighlightBehavior=False,
                highlightColor="#F7A7A6",  # or "blue"
                collapsible=False,
                node={'labelProperty': 'label'},
            )
        graph = stag.agraph(nodes=nodes, edges=edges, config=config)
