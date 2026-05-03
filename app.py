import streamlit as st
import time
import base64

# Configuración principal
st.set_page_config(page_title="Jornadas Deportivas", layout="wide")

# --- 1. CSS: COLORES, ANIMACIÓN Y SCROLL HORIZONTAL FUERTE ---
css = """
<style>
/* Colores principales */
h1, h2, h3 { color: #1a237e; } /* Azul oscuro */
h4 { color: #d32f2f; margin-bottom: 5px; } /* Rojo */
hr { border-top: 3px solid #d32f2f; }

/* Botones principales y de detalles */
div[data-testid="stButton"] > button {
    background-color: #1a237e;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    transition: 0.3s;
    width: 100%;
    height: auto; /* Permite que el botón se adapte al texto */
    padding: 10px 5px; 
}

/* Ajuste de texto para los botones */
div[data-testid="stButton"] > button p {
    font-size: 15px !important; 
    word-break: normal !important; /* Prohíbe romper las palabras por la mitad */
    white-space: normal !important;
}

div[data-testid="stButton"] > button:hover {
    background-color: #d32f2f;
    color: white;
}

/* --- TRUCO DEFINITIVO PARA EL SCROLL HORIZONTAL --- */
/* Forzamos a que el contenedor NO aplaste los elementos y muestre el scroll */
[data-testid="stHorizontalBlock"] {
    flex-wrap: nowrap !important;
    overflow-x: auto !important;
    padding-bottom: 15px;
    -webkit-overflow-scrolling: touch; /* Scroll suave para iPad y celulares */
}

/* Obligamos a cada columna a tener un ancho mínimo estricto */
[data-testid="column"] {
    min-width: 140px !important; 
    width: 140px !important;
    flex: 0 0 140px !important; /* Prohíbe que Streamlit encoja la columna */
    text-align: center;
}

/* Animación del splash screen */
.spin-logo {
    animation: spin 1.5s linear infinite;
    width: 150px;
    display: block;
    margin: 0 auto;
}
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Ajuste de las tarjetas */
div[data-testid="stVerticalBlock"] > div[style*="border"] {
    border-left: 5px solid #1a237e !important;
    border-radius: 10px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- 2. PANTALLA DE CARGA (SPLASH SCREEN) ---
pantalla_carga = st.empty()

with pantalla_carga.container():
    try:
        # Usamos el logo principal a color para la carga
        with open("logo.png", "rb") as f:
            img_data = base64.b64encode(f.read()).decode()
        img_html = f'<img src="data:image/png;base64,{img_data}" class="spin-logo">'
    except FileNotFoundError:
        img_html = '<div class="spin-logo" style="font-size:50px; text-align:center;">⚽</div>'
        st.warning("⚠️ Asegúrate de tener el archivo 'logo.png' en esta carpeta.")

    html_loader = f"""
    <div style="display: flex; justify-content: center; align-items: center; height: 60vh; flex-direction: column;">
        {img_html}
        <h3 style="color: #1a237e; margin-top: 25px;">Cargando calendario...</h3>
    </div>
    """
    st.markdown(html_loader, unsafe_allow_html=True)

time.sleep(2.5)
pantalla_carga.empty()


# --- 3. PÁGINA PRINCIPAL ---
st.title("🏆 Jornadas Deportivas - Hoy")

# --- SCROLL HORIZONTAL DE EQUIPOS ---
st.markdown("### Equipos Participantes")

# Lista corregida con "Sígsig Sporting"
equipos = [
    "San Sebastián", "Dangers", "Estudiantes", "Llactazhungo", 
    "Profesionales", "Sauces", "Siete Estrellas", "Sigsales", 
    "Sígsig Sporting", "Cutchil", "Güel", "San Bartolomé"
]

cols_equipos = st.columns(len(equipos))

for i, col in enumerate(cols_equipos):
    with col:
        # Usamos el logo de prueba en blanco para los equipos
        try:
            st.image("prueba_logo.png", use_container_width=True)
        except:
            st.write("🖼️")
        st.button(equipos[i], key=f"btn_eq_{i}")

st.divider()

# --- TARJETAS DE PARTIDOS ---
st.subheader("📅 Partidos Programados")

# 1. Fulbito - Sub 12
with st.container(border=True):
    st.markdown("#### ⚽ Fulbito - Sub 12")
    st.write("🕒 **14:00** | Profesionales vs. San Sebastián")
    st.write("🕒 **15:00** | Dangers vs. Cutchil")
    st.button("Ver más detalles", key="detalles_f_sub12")

st.write("")

# 2. Fulbito - Sub 15
with st.container(border=True):
    st.markdown("#### ⚽ Fulbito - Sub 15")
    st.write("🕒 **16:00** | Estudiantes vs. Güel")
    st.write("🕒 **17:00** | Llactazhungo vs. Sauces")
    st.button("Ver más detalles", key="detalles_f_sub15")

st.write("")

# 3. Indor - Masculino
with st.container(border=True):
    st.markdown("#### 🥅 Indor - Masculino")
    st.write("🕒 **18:00** | Sigsales vs. San Bartolomé")
    st.write("🕒 **19:00** | Siete Estrellas vs. Sígsig Sporting")
    st.button("Ver más detalles", key="detalles_i_masc")

st.write("")

# 4. Indor - Femenino
with st.container(border=True):
    st.markdown("#### 🥅 Indor - Femenino")
    st.write("🕒 **20:00** | Profesionales vs. Estudiantes")
    st.button("Ver más detalles", key="detalles_i_fem")

st.write("")

# 5. Ecuavoley - Masculino
with st.container(border=True):
    st.markdown("#### 🏐 Ecuavoley - Masculino")
    st.write("🕒 **18:30** | Dangers vs. Llactazhungo")
    st.write("🕒 **19:30** | Cutchil vs. Sauces")
    st.button("Ver más detalles", key="detalles_e_masc")

st.write("")

# 6. Ecuavoley - Femenino
with st.container(border=True):
    st.markdown("#### 🏐 Ecuavoley - Femenino")
    st.write("🕒 **20:30** | San Sebastián vs. San Bartolomé")
    st.button("Ver más detalles", key="detalles_e_fem")
