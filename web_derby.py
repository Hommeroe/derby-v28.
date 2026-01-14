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
st.set_page_config(page_title="DERBY V28", layout="wide")

st.markdown("""
    <style>
    .pelea-card { background-color: #1e1e1e; border: 2px solid #444; border-radius: 10px; padding: 12px; margin-bottom: 20px; color: white; }
    .rojo-text { color: #ff4b4b; font-weight: bold; font-size: 16px; }
    .verde-text { color: #00c853; font-weight: bold; font-size: 16px; text-align: right; }
    .fila-principal { display: flex; justify-content: space-between; align-items: flex-start; }
    .lado { width: 42%; }
    .centro-vs { width: 16%; text-align: center; }
    .btn-check { border: 1px solid #777; padding: 2px 5px; border-radius: 3px; font-size: 11px; display: inline-block; margin-top: 5px; background: #222; }
    .info-sub { font-size: 12px; color: #bbb; margin-top: 2px; }
    .dif-text { text-align: center; font-size: 10px; color: #666; border-top: 1px solid #333; margin-top: 10px; padding-top: 5px; }
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
                    try: partidos.append({"PARTIDO": p[0], "P1": float(p[1]), "P2": float(p[2]), "P3": float(p[3]), "P4": float(p[4])})
                    except: continue
    return partidos

def guardar_todos(lista):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        for p in lista: f.write(f"{p['PARTIDO']}|{p['P1']}|{p['P2']}|{p['P3']}|{p['P4']}\n")

def generar_cotejo_justo(lista_original):
    lista = lista_original.copy()
    cotejo = []
    while len(lista) >= 2:
        rojo = lista.pop(0)
        encontrado = False
        for i in range(len(lista)):
            if lista[i]['PARTIDO'] != rojo['PARTIDO']:
                verde = lista.pop(i); cotejo.append((rojo, verde)); encontrado = True; break
        if not encontrado:
            verde = lista.pop(0); cotejo.append((rojo, verde))
    return cotejo

# --- 3. INTERFAZ ---
tab1, tab2 = st.tabs(["📝 REGISTRO", "🏆 COTEJO"])

with tab1:
    st.title("Registro de Partidos")
    partidos = cargar_datos()
    
    col1, col2 = st.columns(2)
    with col1:
        # Formulario con validación de rango
        with st.form("mi_formulario", clear_on_submit=True):
            st.info("Rango permitido: 1800g a 2680g")
            n = st.text_input("Nombre del Partido:").upper()
            
            # Ajuste de rango: min_value y max_value
            p1 = st.number_input("Peso 1", min_value=1800.0, max_value=2680.0, value=1800.0, step=1.0, format="%.3f")
            p2 = st.number_input("Peso 2", min_value=1800.0, max_value=2680.0, value=1800.0, step=1.0, format="%.3f")
            p3 = st.number_input("Peso 3", min_value=1800.0, max_value=2680.0, value=1800.0, step=1.0, format="%.3f")
            p4 = st.number_input("Peso 4", min_value=1800.0, max_value=2680.0, value=1800.0, step=1.0, format="%.3f")
            
            submit = st.form_submit_button("💾 GUARDAR REGISTRO")
            
            if submit:
                if n:
                    partidos.append({"PARTIDO": n, "P1": p1, "P2": p2, "P3": p3, "P4": p4})
                    guardar_todos(partidos)
                    st.success(f"¡{n} Guardado con éxito!")
                    st.rerun()
                else:
                    st.error("Por favor, ingresa el nombre del partido.")
    
    with col2:
        st.subheader("Lista Actual")
        if partidos:
            st.dataframe(pd.DataFrame(partidos), use_container_width=True)
            if st.button("🗑️ BORRAR TODO"):
                if os.path.exists(DB_FILE): os.remove(DB_FILE)
                st.rerun()

with tab2:
    partidos = cargar_datos()
    if len(partidos) >= 2:
        peleas = generar_cotejo_justo(partidos)
        for r in range(1, 5):
            st.markdown(f"### RONDA {r}")
            col_p = f"P{r}"
            for i, (roj, ver) in enumerate(peleas):
                dif = abs(roj[col_p] - ver[col_p])
                st.markdown(f"""
                <div class="pelea-card">
                    <div style="text-align: center; font-size: 10px; color: #888; margin-bottom: 8px;">PELEA #{i+1}</div>
                    <div class="fila-principal">
                        <div class="lado">
                            <div class="rojo-text">{roj['PARTIDO']}</div>
                            <div class="info-sub">P: {roj[col_p]:.3f} | A: {(i*2)+1:03}</div>
                            <div class="btn-check">G [ ]</div>
                        </div>
                        <div class="centro-vs">
                            <div style="font-weight: bold; font-size: 14px;">VS</div>
                            <div class="btn-check" style="margin-top:10px;">E [ ]</div>
                        </div>
                        <div class="lado" style="text-align: right;">
                            <div class="verde-text">{ver['PARTIDO']}</div>
                            <div class="info-sub">P: {ver[col_p]:.3f} | A: {(i*2)+2:03}</div>
                            <div class="btn-check">G [ ]</div>
                        </div>
                    </div>
                    <div class="dif-text">DIFERENCIA: {dif:.3f}</div>
                </div>
                """, unsafe_allow_html=True)
