import streamlit as st
import time
import base64

# --- CONFIGURACIÓN PRINCIPAL ---
st.set_page_config(page_title="Torneo General - Calendario", layout="wide")

# --- CSS: DISEÑO DARK MODE DEPORTIVO ---
css = """
<style>
.stApp { background-color: #0f172a; }
h1, h2, h3, h4, p, span, div { color: #f8fafc; } 
h1, h2, h3 { font-weight: 800 !important; }

/* --- CABECERA GENERAL --- */
.header-top-bar {
    background: linear-gradient(180deg, #991b1b 0%, #7f1d1d 100%);
    border-bottom: 2px solid #ef4444;
    height: 60px;
    width: 100%;
    margin-top: -60px; 
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.5);
}
.header-title {
    text-align: center;
    color: #ffffff;
    font-weight: 800;
    font-size: 18px;
    letter-spacing: 1px;
}

/* --- CARRUSEL --- */
.carrusel-container {
    background-color: #1e293b; 
    border-radius: 12px;
    border: 1px solid #334155;
    padding: 15px 5px 5px 5px;
    margin-bottom: 20px;
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
    color: #cbd5e1 !important;
    font-size: 11px !important;
    white-space: normal !important;
    line-height: 1.1 !important;
    text-align: center !important;
}

/* --- ESTILOS DE TARJETAS --- */
.dia-titulo {
    color: #ffffff;
    font-size: 26px;
    font-weight: 800;
    margin-top: 20px;
    margin-bottom: 15px;
    border-bottom: 2px solid #ef4444;
    padding-bottom: 5px;
}
div[data-testid="stVerticalBlock"] > div[style*="border"] {
    background-color: #1e3a8a !important; 
    border: 2px solid #38bdf8 !important; 
    border-radius: 12px !important;
    box-shadow: 0 6px 15px rgba(56, 189, 248, 0.2) !important; 
    padding: 0 !important; 
    overflow: hidden;
}
.tarjeta-header {
    background: linear-gradient(180deg, #b91c1c 0%, #991b1b 100%);
    color: #ffffff;
    padding: 10px 15px;
    font-weight: bold;
    font-size: 16px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #f87171;
}
.tarjeta-content { padding: 15px; }

/* --- FILAS DE PARTIDOS --- */
.partido-fila {
    font-size: 14px;
    color: #f1f5f9;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    border-bottom: 1px solid #3b82f6; 
    padding-bottom: 8px;
}
.partido-info { flex: 1; color: #f8fafc; }
.partido-marcador { font-weight: bold; color: #bae6fd; margin-left: 10px; text-align: right;}

/* --- BOTONES --- */
.btn-rojo button {
    background: linear-gradient(180deg, #dc2626 0%, #991b1b 100%) !important;
    border: 1px solid #f87171 !important;
    color: white !important;
    border-radius: 20px !important;
    font-weight: bold !important;
    width: 100% !important;
    padding: 10px !important;
    margin-top: 10px !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
}
.btn-rojo button:hover { background: #7f1d1d !important; }

/* Flecha de volver */
.btn-back button {
    background-color: transparent !important;
    color: #38bdf8 !important;
    border: 2px solid #38bdf8 !important;
    border-radius: 8px !important;
    font-size: 16px !important;
    padding: 5px 15px !important;
    font-weight: bold !important;
    margin-bottom: 15px !important;
    transition: 0.3s;
}
.btn-back button:hover { background-color: #38bdf8 !important; color: #0f172a !important; }

/* Modal oscuro */
div[data-testid="stDialog"] header { display: none !important; }
div[data-testid="stDialog"] { padding-top: 20px !important; background-color: #0f172a !important; }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- DATOS: EQUIPOS, GRUPOS Y PARTIDOS ---
equipos = ["San Sebastián", "Dangers", "Estudiantes", "Llactazhungo", "Profesionales", "Sauces", "Siete Estrellas", "Sigsales", "Sígsig Sporting", "Cutchil", "Güel", "San Bartolomé"]

grupos_data = {
    "Grupo A": [
        {"nombre": "Cutchil", "p": 3, "gf": 3, "gc": 0, "dg": "+3"},
        {"nombre": "Profesionales", "p": 3, "gf": 2, "gc": 1, "dg": "+1"},
        {"nombre": "Estudiantes", "p": 1, "gf": 1, "gc": 2, "dg": "-1"},
        {"nombre": "San Bartolomé", "p": 0, "gf": 0, "gc": 3, "dg": "-3"}
    ],
    "Grupo B": [
        {"nombre": "Dangers", "p": 3, "gf": 4, "gc": 1, "dg": "+3"},
        {"nombre": "San Sebastián", "p": 3, "gf": 2, "gc": 0, "dg": "+2"},
        {"nombre": "Güel", "p": 0, "gf": 1, "gc": 2, "dg": "-1"},
        {"nombre": "Sigsales", "p": 0, "gf": 0, "gc": 4, "dg": "-4"}
    ],
    "Grupo C": [
        {"nombre": "Sígsig Sporting", "p": 3, "gf": 1, "gc": 0, "dg": "+1"},
        {"nombre": "Llactazhungo", "p": 1, "gf": 2, "gc": 2, "dg": "0"},
        {"nombre": "Sauces", "p": 1, "gf": 2, "gc": 2, "dg": "0"},
        {"nombre": "Siete Estrellas", "p": 0, "gf": 0, "gc": 1, "dg": "-1"}
    ]
}

datos_torneo = {
    "Lunes (Ayer)": [
        {"deporte": "⚽ Fulbito - Sub 12", "partidos": [
            {"hora": "14:00", "eq1": "Profesionales", "eq2": "San Sebastián", "marcador": "2 - 1"},
            {"hora": "15:00", "eq1": "Dangers", "eq2": "Cutchil", "marcador": "0 - 3"},
            {"hora": "16:00", "eq1": "Estudiantes", "eq2": "San Bartolomé", "marcador": "1 - 1"}
        ]},
        {"deporte": "🏐 Ecuavoley - Masculino", "partidos": [
            {"hora": "18:00", "eq1": "Sigsales", "eq2": "Sígsig Sporting", "marcador": "2 - 0"},
            {"hora": "19:00", "eq1": "Güel", "eq2": "San Bartolomé", "marcador": "1 - 2"},
            {"hora": "20:00", "eq1": "Sauces", "eq2": "Llactazhungo", "marcador": "2 - 1"}
        ]}
    ],
    "Martes (Hoy)": [
        {"deporte": "⚽ Fulbito - Sub 12", "partidos": [
            {"hora": "14:00", "eq1": "Llactazhungo", "eq2": "San Bartolomé", "marcador": "Pendiente"},
            {"hora": "15:00", "eq1": "Sígsig Sporting", "eq2": "Siete Estrellas", "marcador": "Pendiente"}
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
        {"deporte": "⚽ Fútbol - Categoría Barrio", "partidos": [
            {"hora": "09:00", "eq1": "Sauces", "eq2": "Güel", "marcador": "Pendiente"},
            {"hora": "10:00", "eq1": "Profesionales", "eq2": "Sigsales", "marcador": "Pendiente"}
        ]},
        {"deporte": "🏀 Básquetbol - Femenino", "partidos": [
            {"hora": "18:00", "eq1": "San Bartolomé", "eq2": "Sígsig Sporting", "marcador": "Pendiente"},
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

# --- FUNCIÓN: DIBUJAR GRUPO ---
def dibujar_grupo(nombre_grupo, equipos_grupo):
    with st.container(border=True):
        st.markdown(f'<div class="tarjeta-header" style="background-color:#374151; background-image:none; color:#ffffff; border-bottom: 2px solid #6b7280;">{nombre_grupo}</div>', unsafe_allow_html=True)
        st.markdown('<div class="tarjeta-content" style="color: #ffffff; padding-top: 10px;">', unsafe_allow_html=True)
        st.markdown('<div style="display:flex; justify-content:space-between; font-weight:bold; font-size:12px; border-bottom:1px solid #3b82f6; padding-bottom:5px; margin-bottom:10px; color:#cbd5e1;"><span style="flex:3;">TEAM</span><span style="flex:1; text-align:center;">P</span><span style="flex:1; text-align:center;">GF</span><span style="flex:1; text-align:center;">GC</span><span style="flex:1; text-align:center;">+/-</span></div>', unsafe_allow_html=True)
        for eq in equipos_grupo:
            # Resaltar en celeste si es el equipo que estamos siguiendo
            color_nombre = "#38bdf8" if st.session_state.filtro_equipo == eq["nombre"] else "#ffffff"
            st.markdown(f'<div style="display:flex; justify-content:space-between; font-size:14px; margin-bottom:10px; border-bottom: 1px solid #1e40af; padding-bottom: 8px;"><span style="flex:3; font-weight:bold; color:{color_nombre};">🛡️ {eq["nombre"]}</span><span style="flex:1; text-align:center; font-weight:bold; color:#ffffff;">{eq["p"]}</span><span style="flex:1; text-align:center; color:#e2e8f0;">{eq["gf"]}</span><span style="flex:1; text-align:center; color:#e2e8f0;">{eq["gc"]}</span><span style="flex:1; text-align:center; color:#e2e8f0;">{eq["dg"]}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.write("")

# --- MODAL OSCURO ---
@st.dialog(" ", width="large")
def modal_calendario(deporte_seleccionado):
    hay_datos = False
    for dia, deportes in datos_torneo.items():
        for dep in deportes:
            if dep["deporte"] == deporte_seleccionado:
                # Si hay filtro de equipo, revisar que participe en este partido
                partidos_a_mostrar = []
                for p in dep["partidos"]:
                    if not st.session_state.filtro_equipo or st.session_state.filtro_equipo in [p["eq1"], p.get("eq2", "")]:
                        partidos_a_mostrar.append(p)
                
                if partidos_a_mostrar:
                    hay_datos = True
                    st.markdown(f"<div style='font-size:14px; font-weight:bold; color:#94a3b8; margin-top:15px; margin-bottom:5px;'>{dia}</div>", unsafe_allow_html=True)
                    for p in partidos_a_mostrar:
                        if "Ajedrez" in deporte_seleccionado or "Ciclismo" in deporte_seleccionado:
                            st.markdown(f"<div style='padding:10px; border:1px solid #334155; border-radius:8px; margin-bottom:10px; background-color: #1e293b;'><span style='color: #f8fafc;'>🕒 {p['hora']} | 📍 {p['eq1']}</span> <br> <span style='color:#ef4444; font-weight:bold;'>{p['marcador']}</span></div>", unsafe_allow_html=True)
                        else:
                            m1, m2 = ("-", "-")
                            estado = "Pendiente"
                            if p['marcador'] != "Pendiente":
                                estado = "Fin"
                                partes = p['marcador'].split("-")
                                if len(partes) == 2:
                                    m1, m2 = partes[0].strip(), partes[1].strip()
                            
                            html_partido = f"""
                            <div style="display: flex; align-items: center; padding: 12px 15px; background-color: #1e293b; border: 1px solid #334155; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                                <div style="flex: 2; display: flex; flex-direction: column;">
                                     <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                                         <span style="font-weight: bold; color: #f8fafc;">🛡️ {p['eq1']}</span>
                                         <span style="font-weight: 900; font-size: 16px; color: #ffffff; margin-right: 15px;">{m1}</span>
                                     </div>
                                     <div style="display: flex; justify-content: space-between;">
                                         <span style="font-weight: bold; color: #f8fafc;">🛡️ {p['eq2']}</span>
                                         <span style="font-weight: 900; font-size: 16px; color: #ffffff; margin-right: 15px;">{m2}</span>
                                     </div>
                                </div>
                                <div style="flex: 1; border-left: 1px solid #475569; padding-left: 15px; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; font-size: 12px; color: #cbd5e1;">
                                    <div style="font-weight: bold; color: {'#94a3b8' if estado == 'Fin' else '#ef4444'};">{estado}</div>
                                    <div>{p['hora']}</div>
                                </div>
                            </div>
                            """
                            st.markdown(html_partido, unsafe_allow_html=True)
    if not hay_datos:
        st.info("No hay más partidos programados para este club en este deporte.")

# --- DIBUJAR CABECERAS ---
def dibujar_cabecera():
    # Franja roja superior
    st.markdown('<div class="header-top-bar"><div class="header-title">TORNEO GENERAL - CALENDARIO</div></div>', unsafe_allow_html=True)
    
    if st.session_state.pantalla_actual == "HOME":
        if st.session_state.filtro_equipo:
            # MODO PERFIL DE CLUB (HOME)
            col_back, col_img, col_text = st.columns([1, 1, 6])
            with col_back:
                st.markdown('<div class="btn-back">', unsafe_allow_html=True)
                if st.button("⬅", key="back_from_profile"):
                    st.session_state.filtro_equipo = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with col_img:
                try:
                    st.image("prueba_logo.png", width=45)
                except:
                    st.write("🛡️")
            with col_text:
                st.markdown(f'<h3 style="color:#38bdf8 !important; margin:0; padding-top:5px;">{st.session_state.filtro_equipo.upper()}</h3>', unsafe_allow_html=True)
            st.divider()
        else:
            # HOME NORMAL (CON CARRUSEL)
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
    
    elif st.session_state.pantalla_actual == "DETALLE":
        # CABECERA DETALLE
        col_back, col_title = st.columns([1, 8])
        with col_back:
            st.markdown('<div class="btn-back">', unsafe_allow_html=True)
            if st.button("⬅", key="back_from_detail"):
                st.session_state.pantalla_actual = "HOME"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with col_title:
            st.markdown(f'<h3 style="margin:0; padding-top:5px;">⚽ {st.session_state.filtro_deporte}</h3>', unsafe_allow_html=True)
            if st.session_state.filtro_equipo:
                st.markdown(f'<p style="color:#38bdf8; font-weight:bold; margin-top:-5px;">Mostrando solo datos de: {st.session_state.filtro_equipo}</p>', unsafe_allow_html=True)
        st.write("")


# --- PANTALLA PRINCIPAL (HOME) ---
if st.session_state.pantalla_actual == "HOME":
    dibujar_cabecera()
    
    for dia, deportes in datos_torneo.items():
        deportes_a_mostrar = []
        for dep in deportes:
            partidos_filtrados = []
            for p in dep["partidos"]:
                # Filtro inteligente de equipos
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
                            st.markdown(f'<div class="partido-fila"><div class="partido-info">{p["hora"]} | {p["eq1"]}</div><div class="partido-marcador" style="color:#ef4444;">{p["marcador"]}</div></div>', unsafe_allow_html=True)
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
    dibujar_cabecera()
    
    # 1. EXTRAMOS LOS PARTIDOS DINÁMICAMENTE PARA ESTA TARJETA
    partidos_resumen = []
    for dia, deportes in datos_torneo.items():
        for dep in deportes:
            if dep["deporte"] == st.session_state.filtro_deporte:
                for p in dep["partidos"]:
                    # Si hay filtro, solo guardamos los de ese equipo
                    if not st.session_state.filtro_equipo or st.session_state.filtro_equipo in [p["eq1"], p.get("eq2", "")]:
                        partidos_resumen.append(p)

    with st.container(border=True):
        st.markdown(f'<div class="tarjeta-header">PARTIDOS</div>', unsafe_allow_html=True)
        st.markdown('<div class="tarjeta-content">', unsafe_allow_html=True)
        
        # Mostramos máximo 3 en el resumen
        for p in partidos_resumen[:3]:
            if "Ajedrez" in st.session_state.filtro_deporte or "Ciclismo" in st.session_state.filtro_deporte:
                st.markdown(f'<div class="partido-fila"><div class="partido-info">{p["hora"]} | {p["eq1"]}</div><div class="partido-marcador" style="color:#ef4444;">{p["marcador"]}</div></div>', unsafe_allow_html=True)
            else:
                texto_vs = f"{p['eq1']} vs. {p['eq2']}" if p['marcador'] == "Pendiente" else f"{p['eq1']} - {p['eq2']}"
                color_texto = "#94a3b8" if p['marcador'] == "Pendiente" else "#f8fafc"
                marcador_disp = "Pendiente" if p['marcador'] == "Pendiente" else p['marcador']
                st.markdown(f'<div class="partido-fila"><div class="partido-info" style="color:{color_texto};">{p["hora"]} | {texto_vs}</div><div class="partido-marcador" style="color:{color_texto};">{marcador_disp}</div></div>', unsafe_allow_html=True)
        
        if not partidos_resumen:
            st.info("No hay partidos para mostrar en este filtro.")

        st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
        if st.button("Ver más partidos", key="abrir_modal"):
            modal_calendario(st.session_state.filtro_deporte)
        st.markdown('</div></div>', unsafe_allow_html=True)

    st.write("")
    
    # 2. TABLAS DE POSICIONES INTELIGENTES
    if "Ajedrez" not in st.session_state.filtro_deporte and "Ciclismo" not in st.session_state.filtro_deporte:
        
        # Si NO hay equipo seleccionado, mostramos todos los grupos
        if not st.session_state.filtro_equipo:
            for nombre_g, equipos_g in grupos_data.items():
                dibujar_grupo(nombre_g, equipos_g)
        
        # Si SÍ hay equipo seleccionado, buscamos su grupo y mostramos SOLO ESE
        else:
            grupo_encontrado = False
            for nombre_g, equipos_g in grupos_data.items():
                # Busca si el equipo seleccionado está dentro de este grupo
                if any(eq["nombre"] == st.session_state.filtro_equipo for eq in equipos_g):
                    dibujar_grupo(nombre_g, equipos_g)
                    grupo_encontrado = True
                    break # Deja de buscar
            
            if not grupo_encontrado:
                 st.warning(f"El equipo {st.session_state.filtro_equipo} no participa en la fase de grupos de esta categoría.")
