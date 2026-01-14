import streamlit as st
import pandas as pd
import os

# --- 1. SEGURIDAD ---
if "autenticado" not in st.session_state:
    st.title("🔐 Acceso Privado")
    password = st.text_input("Clave del Palenque:", type="password")
    if st.button("Entrar"):
        if password == "2026":
            st.session_state["autenticado"] = True
            st.rerun()
    st.stop()

# --- 2. CONFIGURACIÓN ---
st.set_page_config(page_title="DERBY V28", layout="centered")

# Estilos para que se vea bien en celular vertical
st.markdown("""
    <style>
    .reportview-container .main .block-container { padding-top: 1rem; }
    .stTable { font-size: 14px !important; }
    .rojo { color: #ff4b4b; font-weight: bold; }
    .verde { color: #00c853; font-weight: bold; }
    .card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        background-color: #f9f9f9;
    }
    </style>
    """, unsafe_allow_html=True)

DB_FILE = "datos_derby.txt"

def cargar_datos():
    partidos = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            for linea in f:
                p = linea.strip().split("|")
                if len(p) == 5:
                    partidos.append({"PARTIDO": p[0], "P1": float(p[1]), "P2": float(p[2]), "P3": float(p[3]), "P4": float(p[4])})
    return partidos

def guardar_todos(lista):
    with open(DB_FILE, "w") as f:
        for p in lista:
            f.write(f"{p['PARTIDO']}|{p['P1']}|{p['P2']}|{p['P3']}|{p['P4']}\n")

# --- 3. REGISTRO ---
st.title("🏆 Derby V28")

with st.expander("➕ REGISTRAR PARTIDO", expanded=False):
    nombre = st.text_input("Nombre del Partido:").upper()
    c1, c2 = st.columns(2)
    with c1:
        p1 = st.number_input("Peso 1", value=0.0, format="%.3f")
        p2 = st.number_input("Peso 2", value=0.0, format="%.3f")
    with c2:
        p3 = st.number_input("Peso 3", value=0.0, format="%.3f")
        p4 = st.number_input("Peso 4", value=0.0, format="%.3f")
    
    if st.button("✅ GUARDAR REGISTRO", use_container_width=True):
        if nombre:
            d = cargar_datos()
            d.append({"PARTIDO": nombre, "P1": p1, "P2": p2, "P3": p3, "P4": p4})
            guardar_todos(d)
            st.success("¡Guardado!")
            st.rerun()

# --- 4. COTEJO POR RONDAS (MODO VERTICAL) ---
partidos = cargar_datos()
if len(partidos) >= 2:
    st.subheader("📋 Cotejo Oficial")
    
    for r in range(1, 5):
        with st.expander(f"🥊 RONDA {r}", expanded=(r==1)):
            col_p = f"P{r}"
            for i in range(0, len(partidos) - 1, 2):
                p_rojo = partidos[i]
                p_verde = partidos[i+1]
                dif = abs(p_rojo[col_p] - p_verde[col_p])
                
                # Formato de tabla limpia para celular
                st.markdown(f"""
                *Pelea #{(i//2)+1}*
                | Lado | Partido | Peso | Anillo |
                | :--- | :--- | :--- | :--- |
                | <span class='rojo'>🔴 ROJO</span> | {p_rojo['PARTIDO']} | {p_rojo[col_p]:.3f} | __ |
                | <span class='verde'>🟢 VERDE</span> | {p_verde['PARTIDO']} | {p_verde[col_p]:.3f} | __ |
                | | | Dif: | {dif:.3f} |
                """, unsafe_allow_html=True)
                st.divider()

    if st.button("🗑️ BORRAR TODO EL DERBY", type="secondary", use_container_width=True):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            st.rerun()
