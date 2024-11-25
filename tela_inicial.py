import streamlit as st

# Configurações iniciais
st.set_page_config(page_title="Ferramentas", 
                   layout="wide")

# Título da página
st.title("Ferramentas de auxílio", anchor=False)
st.write("---------------------------------------------")

# Texto grande após o st.write
texto_grande = """
Este site simples compila um conjunto de ferramentas para tratamento e enriquecimento de dados voltados para análise
de dados e consolidação de resultados.

Ferramentas como:
- Categorizador com IA;
- Consolidador de planilhas;
"""

st.markdown(texto_grande)
