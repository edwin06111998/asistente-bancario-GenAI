import streamlit as st
from html import escape
from ms_eva.services.UtilService import *
from ms_eva.services.GraphService import *
from ms_eva.services.VectorStoreFEService import *
from ms_eva.db.serviceDb import crear_base_de_datos

st.set_page_config(page_title="Chatbot GenAI Demo BG", page_icon="images/logo.png", layout="wide")
st.title("Chatbot GenAI Demo BG")

LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/5/5e/Logo_bg_2020.png"

# Estilo con CSS para el logo arriba a la derecha
st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h1 style="margin: 0; color: #e6007e;">Asistente Bancario</h1>
        <img src="{LOGO_URL}" alt="logo" width="240" style="margin-right: 10px;" />
    </div>
    <hr style="border: 1px solid #e6007e;">
""", unsafe_allow_html=True)

# Sección de sesión
session_id = st.text_input("ID de Sesión (puede colocar cualquier caracter alfanumérico)", value="123456")

# Sección de entrada del usuario
user_input = st.text_area("Escribe tu mensaje:", height=100)

# Botón para procesar
if st.button("Enviar mensaje"):
    if user_input and session_id:
        with st.spinner("Procesando..."):
            try:
                response = processQuery(user_input, session_id)
                save_redis_history(user_input, response["data"], session_id)
                respuesta_limpia = escape(response["data"])
                st.markdown(f"""
                    <div style="margin-top: 1rem;">
                        <strong>Respuesta:</strong>
                        <div style="margin-top: 0.5rem; font-size: 16px; line-height: 1.6;">
                            {respuesta_limpia}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.warning("Debes ingresar un mensaje y un ID de sesión.")

# --- Otras herramientas ---
st.sidebar.header("🔧 Acciones")

if st.sidebar.button("🧹 Limpiar historial"):
    try:
        clear_redis_history(session_id)
        clear_state(session_id)
        st.sidebar.success("Historial limpio.")
    except Exception as e:
        st.sidebar.error(f"Error al limpiar: {e}")

if st.sidebar.button("📥 Cargar Embeddings"):
    try:
        loadEmbedding()
        st.sidebar.success("Embeddings cargados.")
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

if st.sidebar.button("🗂 Crear Base de Datos"):
    try:
        crear_base_de_datos()
        st.sidebar.success("Base de datos creada.")
    except Exception as e:
        st.sidebar.error(f"Error al crear la BD: {e}")