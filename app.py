import streamlit as st
import time
import base64

# Configuración principal
st.set_page_config(page_title="Jornadas Deportivas", layout="wide")

# --- 1. CSS: CARRUSEL UNIFICADO PARA TODOS LOS DISPOSITIVOS ---
css = """
<style>
/* Colores principales */
h1, h2, h3 { color: #1a237e; } 
h4 { color: #d32f2f; margin-bottom: 5px; } 
hr { border-top: 3px solid #d32f2f; }

/* --- CARRUSEL MANUAL (IGNORA LAS COLUMNAS DE STREAMLIT) --- */
.carrusel-equipos {
    display: flex;
    flex-wrap: nowrap;
    overflow-x: auto;
    gap: 10px; /* ESTE ES EL ESPACIO FIJO ENTRE LOGOS PARA TODAS LAS PANTALLAS */
    padding-bottom: 15px;
    -webkit-overflow-scrolling: touch; /* Scroll suave en móviles */
    align-items: flex-end; /* Alinea por abajo por si hay nombres largos */
}

/* Tarjeta individual de cada equipo en el carrusel */
.equipo-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 80px; /* Ancho fijo de la tarjeta */
    width: 80px;
}

/* El logo dentro del carrusel */
.equipo-logo {
    width: 70px; /* Tamaño del escudo */
    height: auto;
    margin-bottom: 5px;
}

/* El botón debajo del logo */
.equipo-card .stButton > button {
    background-color: #1a237e;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    width: 100%;
    padding: 6px 2px;
}
.equipo-card .stButton > button:hover {
    background-color: #d32f2f;
}
.equipo-card .stButton > button p {
    font-size: 12px !important; 
    text-align: center !important; 
    word-break: normal !important; 
    white-space: normal !important;
    line-height: 1.1 !important; 
    margin: 0 auto; 
}

/* Botones de las tarjetas de partidos (mantienen su tamaño normal) */
div[data-testid="stVerticalBlock"] .stButton > button {
    background-color: #1a237e;
    color: white;
    border-radius: 8px;
    transition: 0.3s;
}
div[data-testid="stVerticalBlock"] .stButton > button:hover {
    background-color: #d32f2f;
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

/* Ajuste de las tarjetas de partidos */
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

# --- SCROLL HORIZONTAL DE EQUIPOS (NUEVO MÉTODO) ---
st.markdown("### Equipos Participantes")

equipos = [
    "San Sebastián", "Dangers", "Estudiantes", "Llactazhungo", 
    "Profesionales", "Sauces", "Siete Estrellas", "Sigsales", 
    "Sígsig Sporting", "Cutchil", "Güel", "San Bartolomé"
]

# Convertimos el logo de prueba a base64 para poder meterlo en nuestro carrusel HTML
try:
    with open("prueba_logo.png", "rb") as f:
        prueba_logo_data = base64.b64encode(f.read()).decode()
    img_src = f"data:image/png;base64,{prueba_logo_data}"
except:
    img_src = "" # Si no encuentra la imagen, quedará en blanco

# Abrimos el contenedor del carrusel
st.markdown('<div class="carrusel-equipos">', unsafe_allow_html=True)

# Creamos las columnas dentro del carrusel una por una
cols_equipos = st.columns(len(equipos))

for i, col in enumerate(cols_equipos):
    with col:
        # Metemos todo en una tarjeta "equipo-card" para que el CSS la controle
        st.markdown(f'''
            <div class="equipo-card">
                <img src="{img_src}" class="equipo-logo" alt="logo">
            </div>
        ''', unsafe_allow_html=True)
        # El botón de Streamlit sigue funcionando normal para los clics
        st.button(equipos[i], key=f"btn_eq_{i}")

# Cerramos el contenedor del carrusel
st.markdown('</div>', unsafe_allow_html=True)

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
