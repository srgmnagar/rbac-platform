import streamlit as st
import requests

BASE_URL = "http://localhost:8000"
HEADERS = {"X-API-Key": "dev-key-12345"}

st.title("RBAC Admin Dashboard")

tab1, tab2, tab3 = st.tabs(["Roles", "Permissions", "User Assignments"])

# --- TAB 1: Roles ---
with tab1:
    st.header("Roles")
    roles = requests.get(f"{BASE_URL}/roles", headers=HEADERS).json()
    st.table(roles)

    st.subheader("Create Role")
    role_name = st.text_input("Role Name")
    role_desc = st.text_input("Role Description")
    if st.button("Create Role"):
        r = requests.post(f"{BASE_URL}/roles", headers=HEADERS, json={"name": role_name, "description": role_desc})
        if r.status_code == 200:
            st.success(f"Role '{role_name}' created!")
        else:
            st.error(r.text)

    st.subheader("Assign Permission to Role")
    perms = requests.get(f"{BASE_URL}/permissions", headers=HEADERS).json()
    role_options = {r["name"]: r["id"] for r in roles}
    perm_options = {p["name"]: p["id"] for p in perms}
    selected_role = st.selectbox("Role", list(role_options.keys()), key="rp_role")
    selected_perm = st.selectbox("Permission", list(perm_options.keys()), key="rp_perm")
    if st.button("Assign Permission"):
        r = requests.post(f"{BASE_URL}/role-permissions", headers=HEADERS, json={"role_id": role_options[selected_role], "permission_id": perm_options[selected_perm]})
        if r.status_code == 200:
            st.success(f"Assigned '{selected_perm}' to '{selected_role}'!")
        else:
            st.error(r.text)

# --- TAB 2: Permissions ---
with tab2:
    st.header("Permissions")
    st.table(perms)

    st.subheader("Create Permission")
    perm_name = st.text_input("Permission Name")
    perm_desc = st.text_input("Permission Description")
    if st.button("Create Permission"):
        r = requests.post(f"{BASE_URL}/permissions", headers=HEADERS, json={"name": perm_name, "description": perm_desc})
        if r.status_code == 200:
            st.success(f"Permission '{perm_name}' created!")
        else:
            st.error(r.text)

# --- TAB 3: User Assignments ---
with tab3:
    st.header("Assign User to Role")
    user_id = st.text_input("User ID (e.g. alice@org.com)")
    selected_role_assign = st.selectbox("Role", list(role_options.keys()), key="ur_role")
    if st.button("Assign User"):
        r = requests.post(f"{BASE_URL}/user-roles", headers=HEADERS, json={"user_id": user_id, "role_id": role_options[selected_role_assign]})
        if r.status_code == 200:
            st.success(f"Assigned '{user_id}' to '{selected_role_assign}'!")
        else:
            st.error(r.text)

    st.subheader("Check User Permissions")
    check_user = st.text_input("User ID to check")
    if st.button("Check"):
        r = requests.get(f"{BASE_URL}/query/user-permissions", headers=HEADERS, params={"user_id": check_user})
        data = r.json()
        st.write(f"Permissions: {data.get('data', [])}")
