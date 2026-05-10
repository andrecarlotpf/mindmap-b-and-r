import json
import streamlit as st

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Mindmap Notion Style",
    layout="centered"
)

# =========================================================
# CSS (estilo Notion-like)
# =========================================================
st.markdown("""
<style>

/* BOTÃO estilo card (FORÇADO) */
div.stButton > button {
    width: 100%;
    text-align: left;
    border-radius: 12px !important;
    padding: 12px !important;

    border: 1px solid #e5e7eb !important;
    background-color: #ffffff !important;

    color: #111827 !important;
    font-size: 15px !important;
    font-weight: 500 !important;

    box-shadow: none !important;
    transition: all 0.15s ease-in-out;
}

/* hover mais Notion-like */
div.stButton > button:hover {
    background-color: #f9fafb !important;
    border-color: #d1d5db !important;
    transform: translateY(-1px);
    box-shadow: 0 2px 10px rgba(0,0,0,0.06) !important;
}

/* remove foco azul padrão */
div.stButton > button:focus {
    outline: none !important;
    box-shadow: none !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================
with open("mindmap.json", "r", encoding="utf-8") as f:
    DATA = json.load(f)


# =========================================================
# SEARCH NODE (recursivo)
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
# SESSION STATE
# =========================================================
if "history" not in st.session_state:
    st.session_state.history = ["Salário Maternidade"]


current_title = st.session_state.history[-1]
current_node = find_node(DATA, current_title)


# =========================================================
# BREADCRUMB (clicável)
# =========================================================
st.markdown("### 📍 Caminho")

cols = st.columns(len(st.session_state.history))

for i, title in enumerate(st.session_state.history):
    with cols[i]:
        if st.button(title, key=f"crumb_{i}"):
            st.session_state.history = st.session_state.history[:i+1]
            st.rerun()


st.divider()


# =========================================================
# NODE CONTENT (estilo Notion doc)
# =========================================================
st.title(current_node["title"])
st.write(current_node.get("content", ""))
st.divider()


# =========================================================
# CHILDREN (mindmap navigation)
# =========================================================
children = current_node.get("children", [])

if children:
    st.subheader("📚 Subtópicos")

    for child in children:
        if st.button(f"➡️ {child['title']}", key=child["title"]):
            st.session_state.history.append(child["title"])
            st.rerun()
else:
    st.info("Esse tópico não possui subníveis.")


st.divider()


# =========================================================
# BACK / HOME
# =========================================================
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
# DEBUG PATH
# =========================================================
st.divider()
st.subheader("🧭 Caminho atual")
st.code(" → ".join(st.session_state.history))