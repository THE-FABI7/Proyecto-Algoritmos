import streamlit as st
from streamlit_option_menu import option_menu
from Data.Probabilidades.LogicaPB import LogicaPB


def main():
    LogicaPB = LogicaPB()


# Configuración del icono
st.set_page_config(
    page_title="Project ADA",
    page_icon="https://www.ucaldas.edu.co/intranet2/wp-content/uploads/2014/10/logo-u2.png",
    layout="wide"
)

# Menú de opciones personalizado con tema oscuro
selected = option_menu(
    menu_title="App Algoritmos",  # Título del menú
    options=["Inicio", "Editar", "Ejecutar", "Herramientas",
             "Ayuda"],  # Opciones del menú
    icons=["house", "pencil", "play", "tools",
           "question-circle"],  # Íconos para cada opción
    menu_icon="cast",  # Ícono del menú
    default_index=0,  # Índice de la opción seleccionada por defecto
    orientation="horizontal",  # Orientación del menú
    styles={
        "container": {"padding": "0!important", "background-color": "#000000"},
        "icon": {"color": "#FFD700", "font-size": "25px"},
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "margin": "0px",
            "color": "#FFFFFF",
        },
        "nav-link-selected": {"background-color": "#892BE1"},
    },
)

if selected == "Inicio":
    selected_option = st.selectbox(
        "Seleccionar opción:",
        ["Nuevo Grafo", "Abrir", "Buscar Nodo", "Cerrar", "Guardar",
            "Guardar Como", "Exportar Datos", "Importar Datos", "Salir"]
    )

if selected == "Ejecutar":
    selected_option = st.selectbox(
        "Seleccionar opción:",
        ["Estrategia1", "Estrategia2"]
    )
    if selected_option == 'Estrategia1':
        opcion = st.radio(
            "Seleccione La matriz con la que desea trabajar", LogicaPB.listaMatrices())
        estados = LogicaPB.retornarEstadosFuturos(
            LogicaPB.datosMatrices(opcion))
        futuros = LogicaPB.retornarEstados(LogicaPB.datosMatrices(opcion))
        nodosG1 = st.multiselect(
            "Seleccione los nodos del estado presente", estados)
        nodosG2 = st.multiselect(
            'Seleccione los nodos del estado futuro:', futuros)
        nodosG1_str = ', '.join(nodosG1)
        aux2_str = ', '.join(nodosG2)
        # Muestra la fórmula de probabilidad condicional con los valores de las variables
        st.latex(
            r'P(\{' + aux2_str + r'\}^{t+1} | \{' + nodosG1_str + r'\}^{t})')
        st.header("Distribución de probabilidad")

if selected == 'Ayuda':
    st.write("### Ayuda")
    st.write("Para obtener ayuda, comuníquese con el administrador del sistema.")
    st.write("Correo: admin@algoritmos.com")

    # Explicación de la aplicación
    st.write("### ¿Qué hace esta aplicación?")
    st.write("""
    Esta aplicación está diseñada para ayudar con el análisis y diseño de algoritmos. 
    Proporciona herramientas para crear, editar y ejecutar algoritmos, así como para 
    importar y exportar datos relacionados con los algoritmos.
    """)

    # Botón para descargar el manual de usuario
    manual_path = "./Data/Docs/manual.pdf"  # Reemplaza con la ruta real del manual
    with open(manual_path, "rb") as file:
        btn = st.download_button(
            label="Descargar Manual de Usuario",
            data=file,
            file_name="manual_de_usuario.pdf",
            mime="application/pdf"
        )


st.write("© 2024 Proyecto ADA. Todos los derechos reservados.")
