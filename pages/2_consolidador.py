import streamlit as st
import pandas as pd
import os
import biblioteca as bib
from io import BytesIO

# Função para salvar e gerar o arquivo Excel em memória
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Consolidado")
        writer.close()
    output.seek(0)
    return output

# Configuração da página Streamlit
st.set_page_config(page_title="Consolidação de Excel", 
                   layout="wide")

# Título da página
st.title("Consolidação de Arquivos Excel", anchor=False)

# Recebe o caminho do diretório
diretorio = st.text_input("Informe o caminho do diretório contendo os arquivos Excel:")

# Se o caminho for válido
if diretorio and os.path.isdir(diretorio):
    # Consolida os arquivos Excel
    df_consolidado = bib.consolidar_excel(diretorio)

    # Verifica se há dados para mostrar
    if not df_consolidado.empty:
        # Exibe uma prévia do dataframe consolidado
        st.write("Prévia do Excel consolidado:")
        st.dataframe(df_consolidado)

        st.download_button(
            label="Baixar arquivo",
            data = to_excel(df_consolidado),
            file_name="consolidado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("Não foi possível consolidar os arquivos devido a colunas inconsistentes.")
else:
    st.error("Caminho inválido. Por favor, forneça um caminho de diretório válido.")