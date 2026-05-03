import streamlit as st
import time
import base64

# Configuración principal
st.set_page_config(page_title="Jornadas Deportivas", layout="wide")

# --- 1. CSS: CORRECCIÓN DE ESPACIOS PARA CELULAR ---
css = """
<style>
/* Colores principales */
h1, h2, h3 { color: #1a237e; } 
h4 { color: #d32f2f; margin-bottom: 5px; } 
hr { border-top: 3px solid #d32f2f; }

/* --- CONTENEDOR DEL BOTÓN Y TEXTO CENTRADO --- */
div[data-testid="stButton"] {
    display: flex;
    justify-content: center;
    width: 100%;
}
div[data-testid="stButton"] > button {
    background-color: #1a237e;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    transition: 0.3s;
    width: 100%;
    padding: 6px 2px;
}
div[data-testid="stButton"] > button p {
    font-size: 13px !important; 
    text-align: center !important; 
    word-break: normal !important; 
    white-space: normal !important;
    line-height: 1.1 !important; /* Ajusta la altura de las líneas del texto */
    margin: 0 auto; 
}
div[data-testid="stButton"] > button:hover {
    background-color: #d32f2f;
    color: white;
}

/* --- TRUCO PARA QUITAR EL ESPACIO EN CELULARES --- */
[data-testid="stHorizontalBlock"] {
    flex-direction: row !important; 
    flex-wrap: nowrap !important;
    overflow-x: auto !important;
    padding-bottom: 15px;
    -webkit-overflow-scrolling: touch; 
    align-items: flex-end; 
    gap: 8px !important; /* REDUCE DRAMÁTICAMENTE EL ESPACIO ENTRE LOGOS */
}

/* Ancho fijo para cada equipo, sin relleno extra */
[data-testid="column"] {
    min-width: 95px !important; /* Un poco más angosto para que se junten */
    width: 95px !important;
    max-width: 95px !important;
    flex: 0 0 95px !important;
    display: flex;
    flex-direction: column;
    align-items: center; 
    padding-left: 2px !important; /* Quita el espacio a la izquierda */
    padding-right: 2px !important; /* Quita el espacio a la derecha */
}

/* Centrar la imagen en la columna */
[data-testid="stImage"] {
    display: flex;
    justify-content: center;
    margin-bottom: 5px;
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
        with open("logo.png", "rb") as f:
            img_data = base64.b64encode(f.read()).decode()
        img_html = f'<img src="data:image/png;base64,{img_data}" class="spin-logo">'
    except FileNotFoundError:
        img_html = '<div class="spin-logo" style="font-size:50px; text-align:center;">⚽</div>'

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

equipos = [
    "San Sebastián", "Dangers", "Estudiantes", "Llactazhungo", 
    "Profesionales", "Sauces", "Siete Estrellas", "Sigsales", 
    "Sígsig Sporting", "Cutchil", "Güel", "San Bartolomé"
]

cols_equipos = st.columns(len(equipos))

for i, col in enumerate(cols_equipos):
    with col:
        # El logo se mantiene fijo en 75px para no estirarse
        try:
            st.image("prueba_logo.png", width=75) 
        except:
            st.write("🖼️")
            
        st.button(equipos[i], key=f"btn_eq_{i}")

st.divider()

# --- TARJETAS DE PARTIDOS ---
st.subheader("📅 Partidos Programados")

with st.container(border=True):
    st.markdown("#### ⚽ Fulbito - Sub 12")
    st.write("🕒 **14:00** | Profesionales vs. San Sebastián")
    st.write("🕒 **15:00** | Dangers vs. Cutchil")
    st.button("Ver más detalles", key="detalles_f_sub12")

st.write("")

with st.container(border=True):
    st.markdown("#### ⚽ Fulbito - Sub 15")
    st.write("🕒 **16:00** | Estudiantes vs. Güel")
    st.write("🕒 **17:00** | Llactazhungo vs. Sauces")
    st.button("Ver más detalles", key="detalles_f_sub15")

st.write("")

with st.container(border=True):
    st.markdown("#### 🥅 Indor - Masculino")
    st.write("🕒 **18:00** | Sigsales vs. San Bartolomé")
    st.write("🕒 **19:00** | Siete Estrellas vs. Sígsig Sporting")
    st.button("Ver más detalles", key="detalles_i_masc")

st.write("")

with st.container(border=True):
    st.markdown("#### 🥅 Indor - Femenino")
    st.write("🕒 **20:00** | Profesionales vs. Estudiantes")
    st.button("Ver más detalles", key="detalles_i_fem")

st.write("")

with st.container(border=True):
    st.markdown("#### 🏐 Ecuavoley - Masculino")
    st.write("🕒 **18:30** | Dangers vs. Llactazhungo")
    st.write("🕒 **19:30** | Cutchil vs. Sauces")
    st.button("Ver más detalles", key="detalles_e_masc")

st.write("")

with st.container(border=True):
    st.markdown("#### 🏐 Ecuavoley - Femenino")
    st.write("🕒 **20:30** | San Sebastián vs. San Bartolomé")
    st.button("Ver más detalles", key="detalles_e_fem")
