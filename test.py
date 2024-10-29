import streamlit as st
from streamlit_agraph import agraph, Config, Node, Edge
import numpy as np
import pandas as pd
from scipy.stats import wasserstein_distance  # EMD

# --- Configuración Inicial de la App ---
st.set_page_config(page_title="División Óptima con EMD", layout="wide")

st.title("División de Sistemas Dinámicos usando EMD")
st.write("Minimización de la diferencia entre particiones utilizando Earth Mover's Distance (EMD).")

# --- Entrada de Datos ---
uploaded_file = st.file_uploader("Sube la Matriz de Transición (TPM) en CSV", type="csv")
if uploaded_file:
    tpm = pd.read_csv(uploaded_file, index_col=0).values
    st.write("Matriz de Transición (TPM):")
    st.dataframe(tpm)

# Entrada de nodos en t, t+1 y background
elements_t = st.text_input("Elementos en t (separados por coma)", "A,B,C,D").split(",")
elements_t1 = st.text_input("Elementos en t+1 (separados por coma)", "A',B',C',D'").split(",")
background_elements = st.text_input("Elementos de Background", "E,F").split(",")

# Validación de entradas
if len(elements_t) != len(elements_t1):
    st.error("El número de elementos en t y t+1 debe coincidir.")
    st.stop()

# --- Función para Marginalizar la TPM ---
def marginalize_distribution(tpm, candidate_indices, background_indices):
    """
    Calcula la distribución marginal sobre los elementos del sistema candidato.
    """
    candidate_tpm = np.delete(tpm, background_indices, axis=0)  # Elimina filas del background
    candidate_tpm = np.delete(candidate_tpm, background_indices, axis=1)  # Elimina columnas

    return np.sum(candidate_tpm, axis=0)  # Distribución marginal acumulada

# --- Algoritmo de Partición Óptima con EMD ---
def emd_partitioning(tpm, elements_t, background_elements):
    """
    Realiza la partición del sistema minimizando la EMD.
    """
    n = len(elements_t)
    V = list(range(n))  # Índices de nodos en V
    W0, W1 = set(), set([V[0]])  # Inicializa W0 vacío y W1 con un elemento arbitrario

    # Índices de los elementos de background
    background_indices = [elements_t.index(e) for e in background_elements if e in elements_t]

    # Distribución completa del sistema
    full_dist = np.sum(tpm, axis=0)

    def calculate_emd(subset):
        """Calcula la EMD entre la distribución marginal del subset y el sistema completo."""
        subset_dist = marginalize_distribution(tpm, list(subset), background_indices)
        return wasserstein_distance(full_dist, subset_dist)

    # Iteración Principal
    for i in range(1, n):
        min_emd = float('inf')
        best_vi = None

        for vi in set(V) - W1:
            emd_value = calculate_emd(W1 | {vi}) - calculate_emd({vi})
            if emd_value < min_emd:
                min_emd = emd_value
                best_vi = vi

        W1.add(best_vi)  # Añadir el mejor vi encontrado a W1

    return W0, W1

# --- Ejecución del Algoritmo y Visualización ---
if st.button("Calcular División Óptima"):
    W0, W1 = emd_partitioning(tpm, elements_t, background_elements)

    # Mostrar Resultados
    st.write("Subconjunto W0:", [elements_t[i] for i in W0])
    st.write("Subconjunto W1:", [elements_t[i] for i in W1])

    # Visualización con AGraph
    nodes = [Node(id=f"{elements_t[i]}", label=f"{elements_t[i]}") for i in range(len(elements_t))]
    edges = [Edge(source=f"{elements_t[i]}", target=f"{elements_t1[i]}") for i in range(len(elements_t))]

    config = Config(width=700, height=500, directed=True, nodeHighlightBehavior=True)
    agraph(nodes=nodes, edges=edges, config=config)

# --- Métrica de Tiempo ---
import time
start_time = time.time()
emd_partitioning(tpm, elements_t, background_elements)
end_time = time.time()
st.write(f"Tiempo de ejecución: {end_time - start_time:.4f} segundos")
