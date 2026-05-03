import streamlit as st
import time
import base64

# --- CONFIGURACIÓN PRINCIPAL ---
st.set_page_config(page_title="Torneo General - Calendario", layout="wide")

# --- CSS: DISEÑO CORREGIDO (SOMBRAS, COLORES Y MODAL) ---
css = """
<style>
.stApp { background-color: #f0f2f6; }
h1, h2, h3 { color: #1a237e !important; } 
h4 { color: #d32f2f !important; margin-bottom: 2px !important;} 

/* --- CABECERA --- */
.header-top-bar {
    background-color: #d32f2f; 
    height: 15px;
    width: 100%;
    margin-top: -60px; 
    margin-bottom: 10px;
}
.header-title {
    text-align: center;
    color: #1a237e;
    font-weight: 800;
    font-size: 14px;
    letter-spacing: 1px;
    margin-bottom: 10px;
}

/* --- CARRUSEL DE EQUIPOS --- */
.carrusel-container {
    background-color: #1a237e;
    border-radius: 12px;
    border: 3px solid #d32f2f;
    padding: 15px 5px 5px 5px;
    margin-bottom: 20px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important; /* SOMBRA AÑADIDA */
}
[data-testid="stHorizontalBlock"] {
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    overflow-x: auto !important;
    overflow-y: hidden !important;
    gap: 5px !important;
    padding-bottom: 10px !important;
    -webkit-overflow-scrolling: touch;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
    min-width: 80px !important;
    max-width: 80px !important;
    flex: 0 0 80px !important;
    display: flex;
    flex-direction: column;
    align-items: center;
}
div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button {
    background-color: transparent !important;
    border: none !important;
    padding: 0 !important;
    width: 100% !important;
}
div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button p {
    color: white !important;
    font-size: 11px !important;
    white-space: normal !important;
    line-height: 1.1 !important;
    text-align: center !important;
}

/* --- BLOQUES DE DÍAS Y TARJETAS (CON ELEVACIÓN) --- */
.dia-titulo {
    color: #1a237e;
    font-size: 28px;
    font-weight: 800;
    margin-top: 20px;
    margin-bottom: 10px;
    border-bottom: 2px solid #d32f2f;
    padding-bottom: 5px;
}
div[data-testid="stVerticalBlock"] > div[style*="border"] {
    background-color: white !important;
    border: 2px solid #1a237e !important;
    border-radius: 12px !important;
    box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important; /* SOMBRA PARA ELEVACIÓN */
    padding: 0 !important; 
    overflow: hidden;
}
.tarjeta-header {
    background-color: #1a237e;
    color: white;
    padding: 10px 15px;
    font-weight: bold;
    font-size: 16px;
    display: flex;
    align-items: center;
}
.tarjeta-content { padding: 15px; }

/* Lista de partidos compacta en HOME */
.partido-fila {
    font-size: 14px;
    color: #333;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    border-bottom: 1px solid #eee;
    padding-bottom: 5px;
}
.partido-info { flex: 1; color: #333; }
.partido-marcador { font-weight: bold; color: #1a237e; margin-left: 10px; text-align: right;}

.btn-rojo button {
    background-color: #d32f2f !important;
    color: white !important;
    border-radius: 20px !important;
    font-weight: bold !important;
    width: 100% !important;
    padding: 8px !important;
    margin-top: 10px !important;
}
.btn-rojo button:hover { background-color: #1a237e !important; }

/* Flecha de volver más visible */
.btn-back button {
    background-color: transparent !important;
    color: #1a237e !important;
    border: none !important;
    font-size: 16px !important;
    padding: 0 !important;
    font-weight: 900 !important;
}

/* OCULTAR TÍTULO DEL CUADRO MODAL (ST.DIALOG) */
div[data-testid="stDialog"] header {
    display: none !important;
}
div[data-testid="stDialog"] {
    padding-top: 20px !important;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- BASE DE DATOS EXTENDIDA (Fulbito todos los días) ---
equipos = ["San Sebastián", "Dangers", "Estudiantes", "Llactazhungo", "Profesionales", "Sauces", "Siete Estrellas", "Sigsales", "Sígsig", "Cutchil", "Güel", "San Bartolomé"]

datos_torneo = {
    "Lunes (Ayer)": [
        {"deporte": "⚽ Fulbito - Sub 12", "partidos": [
            {"hora": "14:00", "eq1": "Profesionales", "eq2": "San Sebastián", "marcador": "2 - 1"},
            {"hora": "15:00", "eq1": "Dangers", "eq2": "Cutchil", "marcador": "0 - 3"},
            {"hora": "16:00", "eq1": "Estudiantes", "eq2": "Atlético", "marcador": "1 - 1"}
        ]},
        {"deporte": "🏐 Ecuavoley - Masculino", "partidos": [
            {"hora": "18:00", "eq1": "Sigsales", "eq2": "Sígsig", "marcador": "2 - 0"},
            {"hora": "19:00", "eq1": "Güel", "eq2": "San Bartolomé", "marcador": "1 - 2"},
            {"hora": "20:00", "eq1": "Sauces", "eq2": "Llactazhungo", "marcador": "2 - 1"}
        ]}
    ],
    "Martes (Hoy)": [
        {"deporte": "⚽ Fulbito - Sub 12", "partidos": [
            {"hora": "14:00", "eq1": "Llactazhungo", "eq2": "San Bartolomé", "marcador": "Pendiente"},
            {"hora": "15:00", "eq1": "Sígsig", "eq2": "Siete Estrellas", "marcador": "Pendiente"}
        ]},
        {"deporte": "🥅 Indor - Masculino", "partidos": [
            {"hora": "14:00", "eq1": "Profesionales", "eq2": "Dangers", "marcador": "5 - 2"},
            {"hora": "15:00", "eq1": "Cutchil", "eq2": "Estudiantes", "marcador": "Pendiente"}
        ]},
        {"deporte": "♟️ Ajedrez (Categoría Única)", "partidos": [
            {"hora": "10:00", "eq1": "Coliseo Parroquial", "eq2": "", "marcador": "🥇 1er: Profesionales | 🥈 2do: Güel"}
        ]}
    ],
    "Miércoles (Mañana)": [
        {"deporte": "⚽ Fulbito - Sub 12", "partidos": [
            {"hora": "09:00", "eq1": "Sauces", "eq2": "Güel", "marcador": "Pendiente"}
        ]},
        {"deporte": "🏀 Básquetbol - Femenino", "partidos": [
            {"hora": "18:00", "eq1": "San Bartolomé", "eq2": "Sígsig", "marcador": "Pendiente"},
            {"hora": "19:00", "eq1": "Sigsales", "eq2": "Sauces", "marcador": "Pendiente"}
        ]},
        {"deporte": "🚴 Ciclismo (Ruta Libre)", "partidos": [
            {"hora": "08:00", "eq1": "Parque Central (Salida)", "eq2": "", "marcador": "Pendiente"}
        ]}
    ]
}

# --- CONTROL DE ESTADOS ---
if "pantalla_actual" not in st.session_state:
    st.session_state.pantalla_actual = "HOME"
if "filtro_equipo" not in st.session_state:
    st.session_state.filtro_equipo = None
if "filtro_deporte" not in st.session_state:
    st.session_state.filtro_deporte = None

# --- FUNCIÓN DEL MODAL OSCURO (ESTILO CHAMPIONS LEAGUE) ---
# Usamos width="large" para que ocupe casi toda la pantalla
@st.dialog(" ", width="large")
def modal_calendario(deporte_seleccionado):
    # Ya no hay título, directo a los partidos
    hay_datos = False
    for dia, deportes in datos_torneo.items():
        for dep in deportes:
            if dep["deporte"] == deporte_seleccionado:
                hay_datos = True
                
                # Etiqueta del Día/Fase
                st.markdown(f"<div style='font-size:14px; font-weight:bold; color:#666; margin-top:15px; margin-bottom:5px;'>{dia}</div>", unsafe_allow_html=True)
                
                for p in dep["partidos"]:
                    if "Ajedrez" in deporte_seleccionado or "Ciclismo" in deporte_seleccionado:
                        st.markdown(f"<div style='padding:10px; border:1px solid #ddd; border-radius:8px; margin-bottom:10px;'>🕒 {p['hora']} | 📍 {p['eq1']} <br> <span style='color:#d32f2f; font-weight:bold;'>{p['marcador']}</span></div>", unsafe_allow_html=True)
                    else:
                        # Extraer marcadores si los hay
                        m1, m2 = ("-", "-")
                        estado = "Pendiente"
                        if p['marcador'] != "Pendiente":
                            estado = "Fin"
                            partes = p['marcador'].split("-")
                            if len(partes) == 2:
                                m1, m2 = partes[0].strip(), partes[1].strip()
                        
                        # --- DISEÑO IDÉNTICO A IMAGE_14 (CHAMPIONS LEAGUE) ---
                        html_partido = f"""
                        <div style="display: flex; align-items: center; padding: 12px 15px; background-color: white; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                            <!-- Lado Izquierdo: Equipos y Marcador -->
                            <div style="flex: 2; display: flex; flex-direction: column;">
                                 <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                                     <span style="font-weight: bold; color: #1a237e;">🛡️ {p['eq1']}</span>
                                     <span style="font-weight: 900; font-size: 16px; color: #333; margin-right: 15px;">{m1}</span>
                                 </div>
                                 <div style="display: flex; justify-content: space-between;">
                                     <span style="font-weight: bold; color: #1a237e;">🛡️ {p['eq2']}</span>
                                     <span style="font-weight: 900; font-size: 16px; color: #333; margin-right: 15px;">{m2}</span>
                                 </div>
                            </div>
                            <!-- Lado Derecho: Rayita vertical (border-left), Estado y Hora -->
                            <div style="flex: 1; border-left: 1px solid #ccc; padding-left: 15px; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; font-size: 12px; color: #666;">
                                <div style="font-weight: bold; color: {'#333' if estado == 'Fin' else '#d32f2f'};">{estado}</div>
                                <div>{p['hora']}</div>
                            </div>
                        </div>
                        """
                        st.markdown(html_partido, unsafe_allow_html=True)
    
    if not hay_datos:
        st.info("No hay más partidos programados.")

# --- DIBUJAR CABECERA ---
def dibujar_cabecera():
    st.markdown('<div class="header-top-bar"></div>', unsafe_allow_html=True)
    if st.session_state.filtro_equipo:
        st.markdown(f'<div class="header-title">SIGUIENDO A: {st.session_state.filtro_equipo.upper()}</div>', unsafe_allow_html=True)
        col_back, _ = st.columns([1, 5])
        with col_back:
            st.markdown('<div class="btn-back">', unsafe_allow_html=True)
            if st.button("← Ver todo"):
                st.session_state.filtro_equipo = None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="header-title">TORNEO GENERAL - CALENDARIO</div>', unsafe_allow_html=True)
        st.markdown('<div class="carrusel-container">', unsafe_allow_html=True)
        cols = st.columns(len(equipos))
        for i, col in enumerate(cols):
            with col:
                try:
                    st.image("prueba_logo.png", width=50)
                except:
                    st.write("🛡️")
                if st.button(equipos[i], key=f"btn_{equipos[i]}"):
                    st.session_state.filtro_equipo = equipos[i]
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- PANTALLA PRINCIPAL (HOME) ---
if st.session_state.pantalla_actual == "HOME":
    dibujar_cabecera()
    
    for dia, deportes in datos_torneo.items():
        deportes_a_mostrar = []
        for dep in deportes:
            partidos_filtrados = []
            for p in dep["partidos"]:
                if not st.session_state.filtro_equipo or st.session_state.filtro_equipo in [p["eq1"], p.get("eq2", "")]:
                    partidos_filtrados.append(p)
            if len(partidos_filtrados) > 0:
                deportes_a_mostrar.append({"deporte": dep["deporte"], "partidos": partidos_filtrados})

        if len(deportes_a_mostrar) > 0:
            st.markdown(f'<div class="dia-titulo">{dia}</div>', unsafe_allow_html=True)
            
            for dep in deportes_a_mostrar:
                with st.container(border=True):
                    st.markdown(f'<div class="tarjeta-header">{dep["deporte"]}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="tarjeta-content">', unsafe_allow_html=True)
                    
                    for p in dep["partidos"]:
                        if "Ajedrez" in dep["deporte"] or "Ciclismo" in dep["deporte"]:
                            st.markdown(f'<div class="partido-fila"><div class="partido-info">{p["hora"]} | {p["eq1"]}</div><div class="partido-marcador" style="color:#d32f2f;">{p["marcador"]}</div></div>', unsafe_allow_html=True)
                        else:
                            texto_vs = f"{p['eq1']} vs. {p['eq2']}" if p['marcador'] == "Pendiente" else f"{p['eq1']} - {p['eq2']}"
                            marcador_display = "" if p['marcador'] == "Pendiente" else p['marcador']
                            st.markdown(f'<div class="partido-fila"><div class="partido-info">{p["hora"]} | {texto_vs}</div><div class="partido-marcador">{marcador_display}</div></div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
                    if st.button("Ver más detalles", key=f"det_{dia}_{dep['deporte']}"):
                        st.session_state.pantalla_actual = "DETALLE"
                        st.session_state.filtro_deporte = dep["deporte"]
                        st.rerun()
                    st.markdown('</div></div>', unsafe_allow_html=True)
                st.write("") 

# --- PANTALLA 2: VISTA DETALLADA ---
elif st.session_state.pantalla_actual == "DETALLE":
    st.markdown('<div class="header-top-bar"></div>', unsafe_allow_html=True)
    
    col_back, col_title = st.columns([1, 5])
    with col_back:
        st.markdown('<div class="btn-back">', unsafe_allow_html=True)
        if st.button("← Volver"):
            st.session_state.pantalla_actual = "HOME"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_title:
        st.markdown(f'<h3 style="margin:0; padding-top:5px;">{st.session_state.filtro_deporte}</h3>', unsafe_allow_html=True)
    
    st.write("")
    
    # Tarjeta Compacta (PARTIDOS)
    with st.container(border=True):
        st.markdown(f'<div class="tarjeta-header">PARTIDOS</div>', unsafe_allow_html=True)
        st.markdown('<div class="tarjeta-content">', unsafe_allow_html=True)
        
        st.markdown('<div class="partido-fila"><div class="partido-info">14:00 | Profesionales - San Sebastián</div><div class="partido-marcador">2 - 1</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="partido-fila"><div class="partido-info">15:00 | Dangers - Cutchil</div><div class="partido-marcador">0 - 3</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="partido-fila"><div class="partido-info" style="color:gray;">16:00 | Estudiantes vs. Atlético</div><div class="partido-marcador" style="color:gray;">Pendiente</div></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
        if st.button("Ver más partidos", key="abrir_modal"):
            modal_calendario(st.session_state.filtro_deporte)
        st.markdown('</div></div>', unsafe_allow_html=True)

    st.write("")
    
    # --- TABLAS DE POSICIONES (3 GRUPOS x 4 CLUBES CON COLORES CORREGIDOS) ---
    def dibujar_grupo(nombre_grupo, equipos_grupo):
        with st.container(border=True):
            st.markdown(f'<div class="tarjeta-header" style="background-color:#e0e0e0; color:#1a237e; border-bottom: 2px solid #ccc;">{nombre_grupo}</div>', unsafe_allow_html=True)
            # Aplicamos color oscuro (#333) al texto para que sea visible
            st.markdown('<div class="tarjeta-content" style="color: #333; padding-top: 10px;">', unsafe_allow_html=True)
            
            # Cabecera de la tabla
            st.markdown('<div style="display:flex; justify-content:space-between; font-weight:bold; font-size:12px; border-bottom:1px solid #ccc; padding-bottom:5px; margin-bottom:10px;"><span style="flex:3;">TEAM</span><span style="flex:1; text-align:center;">P</span><span style="flex:1; text-align:center;">GF</span><span style="flex:1; text-align:center;">GC</span><span style="flex:1; text-align:center;">+/-</span></div>', unsafe_allow_html=True)
            
            # Filas de equipos
            for eq in equipos_grupo:
                st.markdown(f'<div style="display:flex; justify-content:space-between; font-size:14px; margin-bottom:10px; border-bottom: 1px solid #eee; padding-bottom: 5px;"><span style="flex:3; font-weight:bold; color:#1a237e;">🛡️ {eq["nombre"]}</span><span style="flex:1; text-align:center; font-weight:bold;">{eq["p"]}</span><span style="flex:1; text-align:center;">{eq["gf"]}</span><span style="flex:1; text-align:center;">{eq["gc"]}</span><span style="flex:1; text-align:center;">{eq["dg"]}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.write("")

    if "Ajedrez" not in st.session_state.filtro_deporte and "Ciclismo" not in st.session_state.filtro_deporte:
        # Grupo A
        dibujar_grupo("Grupo A", [
            {"nombre": "Cutchil", "p": 3, "gf": 3, "gc": 0, "dg": "+3"},
            {"nombre": "Profesionales", "p": 3, "gf": 2, "gc": 1, "dg": "+1"},
            {"nombre": "Estudiantes", "p": 1, "gf": 1, "gc": 1, "dg": "0"},
            {"nombre": "Atlético", "p": 0, "gf": 0, "gc": 3, "dg": "-3"}
        ])
        
        # Grupo B
        dibujar_grupo("Grupo B", [
            {"nombre": "Dangers", "p": 3, "gf": 4, "gc": 1, "dg": "+3"},
            {"nombre": "San Sebastián", "p": 3, "gf": 2, "gc": 0, "dg": "+2"},
            {"nombre": "Güel", "p": 0, "gf": 1, "gc": 2, "dg": "-1"},
            {"nombre": "Sigsales", "p": 0, "gf": 0, "gc": 4, "dg": "-4"}
        ])
        
        # Grupo C
        dibujar_grupo("Grupo C", [
            {"nombre": "Sígsig", "p": 3, "gf": 1, "gc": 0, "dg": "+1"},
            {"nombre": "Llactazhungo", "p": 1, "gf": 2, "gc": 2, "dg": "0"},
            {"nombre": "Sauces", "p": 1, "gf": 2, "gc": 2, "dg": "0"},
            {"nombre": "San Bartolomé", "p": 0, "gf": 0, "gc": 1, "dg": "-1"}
        ])
