import streamlit as st
from streamlit_option_menu import option_menu

# Configuración del icono
st.set_page_config(
    page_title="Project ADA",
    page_icon="https://www.ucaldas.edu.co/portal/wp-content/uploads/2020/05/monitorias-1.jpg",
    layout="wide"
)

# Menú de opciones personalizado con tema oscuro
selected = option_menu(
    menu_title="App Algoritmos",  # Título del menú
    options=["Archivo", "Editar", "Ejecutar", "Herramientas", "Ventana", "Ayuda"],  # Opciones del menú
    icons=["file", "pencil", "play", "tools", "window", "question-circle"],  # Íconos para cada opción
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

if selected == "Archivo":
            selected_option = st.selectbox(
                "Seleccionar opción:",
                ["Nuevo Grafo", "Abrir", "Buscar Nodo", "Cerrar", "Guardar", "Guardar Como", "Exportar Datos", "Importar Datos", "Salir"]
            )
