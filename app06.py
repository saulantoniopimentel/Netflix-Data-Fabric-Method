# python3 -m streamlit run app06.py
# pip install pandas streamlit

import json
import pandas as pd
import streamlit as st

def run_app():
    st.title("Bienvenido al Consumo de Datos")

    user_info = None
    user_name = ""

    with st.sidebar:
        st.header("Autenticación de Usuario")
        user_name = st.text_input("Ingresa tu usuario:")
        st.button("Validar", on_click=click_button)

    if st.session_state.clicked:
        user_info = valida_usuario(user_name)

        if not user_info:
            st.error("❌ Usuario no encontrado o sin acceso.")
            return

        st.success(f"✅ Usuario válido: {user_name}")
        procesar_acceso(user_info)

def valida_usuario(user_name):
    with open('users.json', 'r') as file:
        users_data = json.load(file)

    for user in users_data['users']:
        if user.get('username').lower() == user_name.lower():
            return user
    return None

def procesar_acceso(user_info):
    # Cargar roles y DD
    with open('roles.json', 'r') as file:
        roles_data = json.load(file)

    with open('DD.json', 'r') as file:
        dd_data = json.load(file)

    role_user = user_info.get("role")
    dds = user_info.get("DDs")

    tag_role = None
    for role in roles_data["roles"]:
        if role.get("role") == role_user:
            tag_role = role.get("tag")
            break

    tag_role_dd1 = None
    if "DD1" in dds:
        for access in dd_data['DD1']:
            if access == tag_role:
                tag_role_dd1 = access
                break

    if not tag_role_dd1:
        st.warning("⚠️ No tienes acceso al DD1 con este rol.")
        return

    data_dd1_role = dd_data["DD1"][tag_role_dd1]

    # Obtener columnas permitidas
    col_access = [item.get("golden_name") for item in data_dd1_role]

    st.info(f"Columnas accesibles para tu rol ({role_user}): {', '.join(col_access)}")

    # Leer CSV
    df_netflix = pd.read_csv("netflix.csv")

    

    df_filtrado = df_netflix[col_access]

    st.subheader("Datos filtrados según tus permisos")
    st.dataframe(df_filtrado)

# Estado para el botón
def click_button():
    st.session_state.clicked = True

# Inicializar sesión
if 'clicked' not in st.session_state:
    st.session_state.clicked = False

if __name__ == "__main__":
    run_app()
