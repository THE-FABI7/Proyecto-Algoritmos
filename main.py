import streamlit as st
from streamlit_option_menu import option_menu
from Data.Probabilidades.LogicaPB import LogicaPB

# Configuración del icono y página
st.set_page_config(
    page_title="Project ADA",
    page_icon="https://www.ucaldas.edu.co/intranet2/wp-content/uploads/2014/10/logo-u2.png",
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
        st.selectbox("Seleccionar opción:", ["Nuevo Grafo", "Abrir", "Buscar Nodo", "Cerrar",
                     "Guardar", "Guardar Como", "Exportar Datos", "Importar Datos", "Salir"])

    elif selected == "Ejecutar":
        handle_execute(logica_pb)

    elif selected == 'Ayuda':
        handle_help()

    st.write("© 2024 Proyecto ADA. Todos los derechos reservados.")


def handle_execute(logica_pb):
    selected_option = st.selectbox("Seleccionar opción:", [
                                   "Estrategia1", "Estrategia2"])
    if selected_option == 'Estrategia1':
        num_nodos = st.selectbox(
            "¿Cuántos nodos quieres trabajar?", ["ejemplos", "N"])
        if num_nodos == "ejemplos":
            # Asegúrate de que listaMatrices() no esté recibiendo ningún argumento
            opciones_matriz = logica_pb.listaMatrices()  # Llamada correcta sin argumentos
            opcion = st.radio(
                "Seleccione la matriz con la que desea trabajar", opciones_matriz)

            estados = logica_pb.retornarEstadosFuturos(
                logica_pb.datosMatrices(opcion))
            futuros = logica_pb.retornarEstados(
                logica_pb.datosMatrices(opcion))
            nodosG1 = st.multiselect(
                "Seleccione los nodos del estado presente", estados)
            nodosG2 = st.multiselect(
                'Seleccione los nodos del estado futuro:', futuros)
            estadoActual = st.selectbox(
                "Seleccione el estado actual", logica_pb.retornarValorActual(nodosG1, nodosG2, opcion))
            nodosG1_str = ', '.join(nodosG1)
            aux2_str = ', '.join(nodosG2)
            st.latex(
                r'P(\{' + aux2_str + r'\}^{t+1} | \{' + nodosG1_str + r'\}^{t})')
            if st.button("Iniciar"):
                st.write("Iniciando estrategia...")
        elif num_nodos == "N":
            opcion = st.select_slider(
                "Seleccione la matriz con la que desea trabajar", list(range(6, 200)))


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
