import streamlit as st
import pandas as pd
import os

# --- 1. SEGURIDAD ---
if "autenticado" not in st.session_state:
    st.title("🔐 Acceso Privado - Derby V28")
    password = st.text_input("Ingresa la clave del Palenque:", type="password")
    if st.button("Entrar"):
        if password == "2026":
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("Clave incorrecta")
    st.stop()

# --- 2. CONFIGURACIÓN ---
st.set_page_config(page_title="SISTEMA DERBY V28", layout="centered")
DB_FILE = "datos_derby.txt"

def cargar_datos():
    partidos = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            for linea in f:
                partes = linea.strip().split("|")
                if len(partes) == 5:
                    partidos.append({
                        "PARTIDO": partes[0],
                        "P1": float(partes[1]), "P2": float(partes[2]),
                        "P3": float(partes[3]), "P4": float(partes[4])
                    })
    return partidos

def guardar_todos(lista_partidos):
    with open(DB_FILE, "w") as f:
        for p in lista_partidos:
            f.write(f"{p['PARTIDO']}|{p['P1']}|{p['P2']}|{p['P3']}|{p['P4']}\n")

# --- 3. INTERFAZ ---
st.title("🏆 Registro de Pesos")

# Formulario de Registro
with st.expander("➕ REGISTRAR NUEVO PARTIDO", expanded=True):
    # Usamos una clave (key) para resetear los inputs
    nombre = st.text_input("Nombre del Partido:", key="n_input").upper()
    c1, c2 = st.columns(2)
    with c1:
        p1 = st.number_input("Peso 1", value=0.0, format="%.3f", step=0.001, key="p1_input")
        p2 = st.number_input("Peso 2", value=0.0, format="%.3f", step=0.001, key="p2_input")
    with c2:
        p3 = st.number_input("Peso 3", value=0.0, format="%.3f", step=0.001, key="p3_input")
        p4 = st.number_input("Peso 4", value=0.0, format="%.3f", step=0.001, key="p4_input")
    
    if st.button("✅ GUARDAR Y LIMPIAR", use_container_width=True):
        if nombre:
            partidos_actuales = cargar_datos()
            nuevo = {"PARTIDO": nombre, "P1": p1, "P2": p2, "P3": p3, "P4": p4}
            partidos_actuales.append(nuevo)
            guardar_todos(partidos_actuales)
            st.success("¡Guardado!")
            st.rerun() # Esto recarga la página y limpia las casillas
        else:
            st.error("Escribe el nombre")

# --- 4. LISTA Y EDICIÓN ---
partidos = cargar_datos()
if partidos:
    st.divider()
    st.subheader("📊 Partidos Registrados")
    
    for i, p in enumerate(partidos):
        with st.expander(f"📌 {p['PARTIDO']}"):
            col_a, col_b = st.columns(2)
            # Inputs para editar directamente
            nuevo_n = st.text_input(f"Editar Nombre", value=p['PARTIDO'], key=f"edit_n_{i}").upper()
            e1 = st.number_input(f"P1", value=p['P1'], format="%.3f", key=f"e1_{i}")
            e2 = st.number_input(f"P2", value=p['P2'], format="%.3f", key=f"e2_{i}")
            e3 = st.number_input(f"P3", value=p['P3'], format="%.3f", key=f"e3_{i}")
            e4 = st.number_input(f"P4", value=p['P4'], format="%.3f", key=f"e4_{i}")
            
            if st.button(f"💾 Actualizar {p['PARTIDO']}", key=f"btn_{i}", use_container_width=True):
                partidos[i] = {"PARTIDO": nuevo_n, "P1": e1, "P2": e2, "P3": e3, "P4": e4}
                guardar_todos(partidos)
                st.rerun()

    st.divider()
    if st.button("🗑️ BORRAR TODO EL DERBY", type="secondary", use_container_width=True):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            st.rerun()
