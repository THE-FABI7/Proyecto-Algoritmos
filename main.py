import streamlit as st
from streamlit_agraph import agraph, Node, Edge
from streamlit_option_menu import option_menu
from src.LogicaPB import LogicaPB
from src.Estrategia1 import Estrategia1
import pandas as pd
from src.gui import Gui

# Configuración del icono y página
st.set_page_config(
    page_title="Grafos",
    page_icon="https://www.ucaldas.edu.co/intranet2/wp-content/uploads/2014/10  /logo-u2.png",
    layout="wide"
)


def load_css():
    with open('styles.css', 'r') as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)


def main():
    # Carga de estilos CSS
    load_css()

    # Instancia de LogicaPB
    logica_pb = LogicaPB()
    interfaz = Gui()
    estrategia1 = Estrategia1()

    # Menú de opciones personalizado con tema oscuro
    selected = option_menu(
        menu_title="App Algoritmos",
        options=["Inicio", "Editar", "Ejecutar", "Herramientas", "Ayuda"],
        icons=["house", "pencil", "play", "tools", "question-circle"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#000000"},
            "icon": {"color": "#FFD700", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "color": "#FFFFFF"},
            "nav-link-selected": {"background-color": "#892BE1"}
        }
    )

    if selected == "Inicio":
        inicio_options = st.selectbox("Seleccionar opción:", ["Cargar TPM", "Buscar Nodo", "Cerrar",
                                                              "Guardar", "Guardar Como", "Exportar Datos", "Importar Datos", "Salir"])
        if inicio_options == 'Cargar TPM':
            st.title("Carga de Matriz de Transición de Probabilidades")
            # Componente para cargar un archivo
            data = st.file_uploader(
                "Cargar matriz de probabilidades", type=['xlsx'])
            if data is not None:
                # Cargar y cachear la matriz
                tpm = load_tpm(data)

                if tpm is not None:
                    st.write("Matriz de Transición de Probabilidades:")
                    st.write(tpm)

                    # Opciones basadas en los datos de la matriz
                    st.sidebar.write("Configuración del Análisis")
                    # Asumiendo que las columnas son los nodos
                    nodes = list(tpm.columns)
                    selected_node = st.sidebar.selectbox(
                        "Escoge un nodo para analizar:", nodes)

    elif selected == "Ejecutar":
        handle_execute(logica_pb, interfaz, estrategia1)

    elif selected == 'Ayuda':
        handle_help()

    st.write("© 2024 Proyecto ADA. Todos los derechos reservados.")


def handle_execute(logica_pb, interfaz, estrategia1):
    selected_option = st.selectbox("Seleccionar opción:", [
                                   "Estrategia1", "Estrategia2"])
    if selected_option == 'Estrategia1':
        num_nodos = st.selectbox(
            "¿Cuántos nodos quieres trabajar?", ["ejemplos", "N"])
        if num_nodos == "ejemplos":
            opciones_matriz = logica_pb.listaMatrices()
            opcion = st.radio(
                "Seleccione la matriz con la que desea trabajar", opciones_matriz)

            candidato = st.multiselect(
                "Seleccione los nodos del sistema candidato", estados)
            futuros = logica_pb.retornarEstadosFuturos(
                logica_pb.datosMatrices(opcion))
            estados = logica_pb.retornarEstados(
                logica_pb.datosMatrices(opcion))

            # condiciones de background a el estado (presente)
            # marginalizar los futuros (estados)
            nodosG1 = st.multiselect(
                "Seleccione los nodos del estado presente", estados)
            nodosG2 = st.multiselect(
                'Seleccione los nodos del estado futuro:', futuros)
            estadoActual = st.selectbox(
                "Seleccione el estado actual", logica_pb.retornarValorActual(nodosG1, nodosG2, opcion))
            aux2 = []
            for i in nodosG2:
                # verificar si el dato tiene ' al final por ejemplo "1'"
                if "'" in i:
                    aux2.append(i[:-1])
            if st.button("Iniciar"):
                st.write("Iniciando estrategia...")
                st.session_state.nodes, st.session_state.edges = interfaz.generar_grafoBipartito(
                    nodosG1, nodosG2, Node, Edge)
                # aux2_str = ', '.join(nodosG2)
                # nodosG1_str = ', '.join(nodosG1)
                # st.latex(
                # r'P(\{' + aux2_str + r'\}^{t+1} | \{' + nodosG1_str + r'\}^{t})')
                aux = estrategia1.distribucion_candidatos(
                    nodosG1, nodosG2, estadoActual, candidato, opcion)
                nodosG1_str = ', '.join(nodosG1)
                aux2_str = ', '.join(nodosG2)
                # Muestra la fórmula de probabilidad condicional con los valores de las variables
                st.header("Distriución de probabilidad original")
                st.latex(
                    r'P(\{' + aux2_str + r'\}^{t+1} | \{' + nodosG1_str + r'\}^{t})')
                st.header(
                    "Distribución de probabilidad despues de elegir el candidato")
                st.table(aux)
                st.header("Mejor particion Sustentación Proyecto")
                particion, d, tiempo, lista = estrategia1.retornar_mejor_particion(
                    nodosG1, nodosG2, estadoActual, candidato, opcion)
                st.write(str(particion), d)
                interfaz.pintarGrafoGenerado(
                    nodosG1, nodosG2, estadoActual, st.session_state.edges, candidato, Node, Edge, opcion)

        elif num_nodos == "N":
            opcion = st.select_slider(
                "Seleccione la cantidad de nodos que desea usar", list(range(6, 200)))
            if st.button("Iniciar"):
                st.write("Iniciando estrategia con ", {opcion}, "nodos...")


# Función para cargar y almacenar la matriz en caché
@st.cache_data
def load_tpm(data):
    if data is not None:
        # Suponiendo que es un archivo excel
        # x
        return pd.read_excel(data)
    else:
        return None


def handle_help():
    st.write("### Ayuda")
    st.write("Para obtener ayuda, comuníquese con el administrador del sistema.")
    st.write("Correo: admin@algoritmos.com")
    st.write("""
    Esta aplicación está diseñada para ayudar con el análisis y diseño de algoritmos.
    Proporciona herramientas para crear, editar y ejecutar algoritmos, así como para
    importar y exportar datos relacionados con los algoritmos.
    """)
    manual_path = "./Data/Docs/manual.pdf"
    with open(manual_path, "rb") as file:
        st.download_button("Descargar Manual de Usuario", data=file,
                           file_name="manual_de_usuario.pdf", mime="application/pdf")


if __name__ == "__main__":
    main()
