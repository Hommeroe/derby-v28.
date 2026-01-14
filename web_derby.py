import streamlit as st
import pandas as pd
import os

# --- 1. SEGURIDAD ---
if "autenticado" not in st.session_state:
    st.title("Acceso Privado")
    password = st.text_input("Clave:", type="password")
    if st.button("Entrar"):
        if password == "2026":
            st.session_state["autenticado"] = True
            st.rerun()
    st.stop()

# --- 2. CONFIGURACION ---
st.set_page_config(page_title="DERBY V28 - INTELIGENTE", layout="wide")

st.markdown("""
    <style>
    @media print {
        .no-print { display: none !important; }
        .print-container { display: flex; flex-wrap: wrap; justify-content: space-between; }
        .pelea-card { width: 48% !important; border: 1px solid #000 !important; margin-bottom: 10px !important; padding: 10px !important; color: black !important; background: white !important; page-break-inside: avoid; }
    }
    .pelea-card { background-color: #1e1e1e; border: 2px solid #444; border-radius: 12px; padding: 15px; margin-bottom: 20px; color: white; font-family: sans-serif; }
    .rojo-text { color: #ff4b4b; font-weight: bold; }
    .verde-text { color: #00c853; font-weight: bold; }
    .alerta { background-color: #ff4b4b; color: white; padding: 5px; border-radius: 5px; text-align: center; font-weight: bold; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

DB_FILE = "datos_derby.txt"

def cargar_datos():
    partidos = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            for linea in f:
                p = linea.strip().split("|")
                if len(p) == 5:
                    try:
                        partidos.append({"PARTIDO": p[0], "P1": float(p[1]), "P2": float(p[2]), "P3": float(p[3]), "P4": float(p[4])})
                    except ValueError: continue
    return partidos

def guardar_todos(lista):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        for p in lista:
            f.write(f"{p['PARTIDO']}|{p['P1']}|{p['P2']}|{p['P3']}|{p['P4']}\n")

# --- FUNCION DE COTEJO INTELIGENTE ---
def generar_cotejo_justo(lista_original):
    lista = lista_original.copy()
    cotejo = []
    while len(lista) >= 2:
        rojo = lista.pop(0)
        # Buscar un verde que no sea del mismo partido
        encontrado = False
        for i in range(len(lista)):
            if lista[i]['PARTIDO'] != rojo['PARTIDO']:
                verde = lista.pop(i)
                cotejo.append((rojo, verde))
                encontrado = True
                break
        if not encontrado: # Si no hay más opciones (al final), se pone el que queda
            verde = lista.pop(0)
            cotejo.append((rojo, verde))
    return cotejo

# --- 3. PESTAÑAS ---
tab1, tab2 = st.tabs(["REGISTRO", "COTEJO INTELIGENTE"])

with tab1:
    st.title("Control de Pesaje")
    partidos = cargar_datos()
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Nuevo Registro")
        n = st.text_input("Nombre del Partido:").upper()
        p1 = st.number_input("Peso 1", format="%.3f", key="p1")
        p2 = st.number_input("Peso 2", format="%.3f", key="p2")
        p3 = st.number_input("Peso 3", format="%.3f", key="p3")
        p4 = st.number_input("Peso 4", format="%.3f", key="p4")
        if st.button("GUARDAR", use_container_width=True):
            if n:
                partidos.append({"PARTIDO": n, "P1": p1, "P2": p2, "P3": p3, "P4": p4})
                guardar_todos(partidos); st.rerun()
    with col2:
        st.subheader("Lista de Partidos")
        if partidos:
            df = pd.DataFrame(partidos)
            df.index = range(1, len(df)+1)
            st.dataframe(df, use_container_width=True)
            if st.button("LIMPIAR DERBY"):
                if os.path.exists(DB_FILE): os.remove(DB_FILE); st.rerun()

with tab2:
    partidos = cargar_datos()
    if len(partidos) >= 2:
        st.title("Hoja de Cotejo Oficial")
        st.markdown('<div class="no-print">', unsafe_allow_html=True)
        modo_impresion = st.checkbox("Vista de Impresion (2 por fila)")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Realizar el cotejo inteligente
        peleas_ordenadas = generar_cotejo_justo(partidos)

        for r in range(1, 5):
            st.header(f"RONDA {r}")
            col_p = f"P{r}"
            st.markdown('<div class="print-container">', unsafe_allow_html=True)
            
            for i, (roj, ver) in enumerate(peleas_ordenadas):
                dif = abs(roj[col_p] - ver[col_p])
                anillo_r = (i * 2) + 1
                anillo_v = (i * 2) + 2
                
                # Alerta si el algoritmo no pudo evitar el mismo partido (solo pasa si ya no hay más gente)
                alerta_html = '<div class="alerta">MISMO PARTIDO - REVISAR</div>' if roj['PARTIDO'] == ver['PARTIDO'] else ""

                st.markdown(f"""
                <div class="pelea-card">
                    <div style="text-align: center; border-bottom: 1px solid #555; margin-bottom: 10px;">
                        <b>PELEA #{i+1}</b>
                    </div>
                    {alerta_html}
                    <div style="margin-bottom: 10px;">
                        <span class="rojo-text">ROJO:</span> {roj['PARTIDO']}<br>
                        Peso: {roj[col_p]:.3f} | Anillo: {anillo_r:03}
                    </div>
                    <div style="text-align: center; margin: 5px 0;">VS</div>
                    <div style="margin-bottom: 10px;">
                        <span class="verde-text">VERDE:</span> {ver['PARTIDO']}<br>
                        Peso: {ver[col_p]:.3f} | Anillo: {anillo_v:03}
                    </div>
                    <div style="text-align: right; font-size: 11px; border-top: 1px solid #555; padding-top: 5px;">
                        DIF: {dif:.3f} | GANADOR: [ ]
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Faltan datos para el cotejo.")
