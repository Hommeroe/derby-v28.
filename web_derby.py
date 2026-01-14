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
st.set_page_config(page_title="DERBY V28 - JUSTO", layout="wide")

st.markdown("""
    <style>
    @media print {
        .no-print { display: none !important; }
        .print-container { display: flex; flex-wrap: wrap; justify-content: space-between; }
        .pelea-card { width: 48% !important; border: 1px solid #000 !important; margin-bottom: 10px !important; padding: 10px !important; color: black !important; background: white !important; page-break-inside: avoid; }
    }
    .pelea-card { background-color: #1e1e1e; border: 2px solid #444; border-radius: 12px; padding: 15px; margin-bottom: 20px; color: white; }
    .alerta { color: #ff4b4b; font-weight: bold; background-color: #ffebeb; padding: 5px; border-radius: 5px; }
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

# --- 3. PESTAÑAS ---
tab1, tab2 = st.tabs(["REGISTRO", "HOJA DE COTEJO"])

with tab1:
    st.title("Control de Pesaje")
    partidos = cargar_datos()
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Nuevo Registro")
        n = st.text_input("Nombre del Partido:").upper()
        p1 = st.number_input("Peso 1", format="%.3f")
        p2 = st.number_input("Peso 2", format="%.3f")
        p3 = st.number_input("Peso 3", format="%.3f")
        p4 = st.number_input("Peso 4", format="%.3f")
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

with tab2:
    partidos = cargar_datos()
    if len(partidos) >= 2:
        st.title("Hoja de Cotejo Oficial")
        modo_impresion = st.checkbox("Vista de Impresion (2 por fila)")
        
        for r in range(1, 5):
            st.markdown(f"## RONDA {r}")
            col_p = f"P{r}"
            st.markdown('<div class="print-container">', unsafe_allow_html=True)
            
            # Lógica de Cotejo
            for i in range(0, len(partidos) - 1, 2):
                roj = partidos[i]
                ver = partidos[i+1]
                
                # ADVERTENCIA SI SON DEL MISMO PARTIDO
                error_mismo_partido = ""
                if roj['PARTIDO'] == ver['PARTIDO']:
                    error_mismo_partido = '<div class="alerta">⚠️ ¡ALERTA: MISMO PARTIDO! REORDENAR</div>'
                
                dif = abs(roj[col_p] - ver[col_p])
                
                st.markdown(f"""
                <div class="pelea-card">
                    <div style="text-align: center; font-weight: bold;">PELEA #{(i//2)+1}</div>
                    {error_mismo_partido}
                    <div style="margin: 10px 0;">
                        <span style="color: #ff4b4b;">ROJO:</span> {roj['PARTIDO']}<br>
                        Peso: {roj[col_p]:.3f} | Anillo: {(i+1):03}
                    </div>
                    <div style="text-align: center;">VS</div>
                    <div style="margin: 10px 0;">
                        <span style="color: #00c853;">VERDE:</span> {ver['PARTIDO']}<br>
                        Peso: {ver[col_p]:.3f} | Anillo: {(i+2):03}
                    </div>
                    <div style="text-align: right; font-size: 11px; border-top: 1px solid #444;">
                        DIF: {dif:.3f} | GANADOR: [ ]
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
