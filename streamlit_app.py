
import json
import streamlit as st


# =========================================================
# Dados do mapa
# =========================================================

with open("mindmap.json", "r", encoding="utf-8") as file:
    DATA = json.load(file)


# =========================================================
# Busca recursiva
# =========================================================

def find_node(node, title):
    if node["title"] == title:
        return node

    for child in node.get("children", []):
        result = find_node(child, title)

        if result:
            return result

    return None


# =========================================================
# Navegação
# =========================================================

if "history" not in st.session_state:
    st.session_state.history = ["Salário Maternidade"]


current_title = st.session_state.history[-1]
current_node = find_node(DATA, current_title)


# =========================================================
# Interface
# =========================================================

st.set_page_config(
    page_title="Mapa Mental Navegável",
    layout="centered"
)

st.title("🧠 Mapa Mental Navegável")

st.divider()

st.header(current_node["title"])

st.write(current_node["content"])

st.divider()

children = current_node.get("children", [])

if children:
    st.subheader("Próximos tópicos")

    for child in children:
        if st.button(f"➡️ {child['title']}"):
            st.session_state.history.append(child["title"])
            st.rerun()

else:
    st.info("Esse tópico não possui subníveis.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    if len(st.session_state.history) > 1:
        if st.button("⬅️ Voltar"):
            st.session_state.history.pop()
            st.rerun()

with col2:
    if st.button("🏠 Início"):
        st.session_state.history = ["Salário Maternidade"]
        st.rerun()


# =========================================================
# Histórico
# =========================================================

st.divider()

st.subheader("Caminho atual")

path = " → ".join(st.session_state.history)

st.code(path)
