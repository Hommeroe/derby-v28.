import streamlit as st
import pandas as pd
import os

# --- 1. SEGURIDAD ---
if "autenticado" not in st.session_state:
    st.title("🔐 Acceso Privado")
    password = st.text_input("Clave:", type="password")
    if st.button("Entrar"):
        if password == "2026":
            st.session_state["autenticado"] = True
            st.rerun()
    st.stop()

# --- 2. CONFIGURACIÓN (Optimizada para Móvil) ---
st.set_page_config(page_title="DERBY V28", layout="centered")

# CSS inyectado para forzar que las tablas no estiren la pantalla
st.markdown("""
    <style>
    .stTable {
        font-size: 12px !important;
    }
    div[data-testid="stExpander"] div[role="button"] p {
        font-size: 14px;
        font-weight: bold;
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
    nombre = st.text_input("Nombre:").upper()
    c1, c2 = st.columns(2)
    with c1:
        p1 = st.number_input("P1", value=0.0, format="%.3f")
        p2 = st.number_input("P2", value=0.0, format="%.3f")
    with c2:
        p3 = st.number_input("P3", value=0.0, format="%.3f")
        p4 = st.number_input("P4", value=0.0, format="%.3f")
    
    if st.button("✅ GUARDAR", use_container_width=True):
        if nombre:
            d = cargar_datos()
            d.append({"PARTIDO": nombre, "P1": p1, "P2": p2, "P3": p3, "P4": p4})
            guardar_todos(d)
            st.rerun()

# --- 4. COTEJO PROFESIONAL (MODO MÓVIL) ---
partidos = cargar_datos()
if len(partidos) >= 2:
    st.subheader("📋 Cotejo por Rondas")
    
    for r in range(1, 5):
        with st.expander(f"🥊 RONDA {r}", expanded=(r==1)):
            col_p = f"P{r}"
            for i in range(0, len(partidos) - 1, 2):
                r_partido = partidos[i]
                v_partido = partidos[i+1]
                dif = abs(r_partido[col_p] - v_partido[col_p])
                
                # Diseño tipo "Card" para que quepa en vertical
                st.markdown(f"""
                *Cotejo { (i//2)+1 }*
                | Lado | Partido | Peso | Anillo |
                | :--- | :--- | :--- | :--- |
                | <span style='color:red'>🔴 ROJO</span> | *{r_partido['PARTIDO']}* | {r_partido[col_p]:.3f} | __ |
                | <span style='color:green'>🟢 VERDE</span> | *{v_partido['PARTIDO']}* | {v_partido[col_p]:.3f} | __ |
                | | | Dif: | {dif:.3f} |
                """)
                st.divider()

    if st.button("🗑️ BORRAR DATOS", type="secondary", use_container_width=True):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            st.rerun()
