import streamlit as st
import time
import base64

# Configuración principal
st.set_page_config(page_title="Jornadas Deportivas", layout="wide")

# --- 1. CSS: COLORES, ANIMACIÓN Y SCROLL HORIZONTAL ---
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
}
div[data-testid="stButton"] > button:hover {
    background-color: #d32f2f;
    color: white;
}

/* --- TRUCO PARA EL SCROLL HORIZONTAL DE EQUIPOS --- */
/* Obliga a las columnas a no saltar de línea y crea una barra de desplazamiento */
div[data-testid="column"] {
    flex: 0 0 auto !important;
    width: 110px !important; /* Ancho de cada logo/botón */
    text-align: center;
}
div[data-testid="stHorizontalBlock"] {
    overflow-x: auto;
    flex-wrap: nowrap;
    padding-bottom: 15px;
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
        with open("prueba_logo.png", "rb") as f:
            img_data = base64.b64encode(f.read()).decode()
        img_html = f'<img src="data:image/png;base64,{img_data}" class="spin-logo">'
    except FileNotFoundError:
        img_html = '<div class="spin-logo" style="font-size:50px; text-align:center;">⚽</div>'
        st.warning("⚠️ Guarda tu imagen como 'prueba_logo.png' en esta carpeta.")

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
    "Sígsig", "Cutchil", "Güel", "San Bartolomé"
]

# Creamos tantas columnas como equipos (el CSS las hará deslizables hacia el lado)
cols_equipos = st.columns(len(equipos))

for i, col in enumerate(cols_equipos):
    with col:
        # Mostramos el logo de prueba en cada equipo
        try:
            st.image("prueba_logo.png", use_container_width=True)
        except:
            st.write("🖼️") # Placeholder si no encuentra la imagen
        # Botón con el nombre corto debajo del logo
        st.button(equipos[i], key=f"btn_eq_{i}")

st.divider()

# --- TARJETAS DE PARTIDOS (ESTILO GOOGLE / JJOO) ---
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
    st.write("🕒 **19:00** | Siete Estrellas vs. Sígsig")
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
