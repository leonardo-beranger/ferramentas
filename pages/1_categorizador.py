import streamlit as st
import pandas as pd
import biblioteca as bib
from io import BytesIO
import os

# Configurações iniciais
st.set_page_config(page_title="Categorizador", 
                   layout="wide")

# Título da página
st.title("Categorizador", anchor=False)
st.write("---------------------------------------------")

col1, col2 = st.columns(2)

with col1:

    # Botão para carregar planilha Excel
    upload_categorizar = st.file_uploader("Carregue sua planilha Excel que será categorizada:", key=1, type=["xlsx", "xls" ,"xlsb", "xlsm"])

    if upload_categorizar:
        try:
            # Carregar a planilha no Pandas
            cat = pd.read_excel(upload_categorizar)
            
            # Exibir uma pré-visualização da planilha
            st.write("Pré-visualização dos dados carregados:")
            st.dataframe(cat.head())

            coluna = st.selectbox('Selecione a coluna que deverá ser categorizada:', cat.columns)

        except Exception as e:
            st.error(f"Erro ao carregar o arquivo: {e}")

with col2:
    # Botão para carregar planilha Excel
    upload_treinamento = st.file_uploader("Carregue sua planilha Excel que será o treinamento da IA:", key=2, type=["xlsx", "xls" ,"xlsb", "xlsm"])

    if upload_treinamento:
        try:
            # Carregar a planilha no Pandas
            trein = pd.read_excel(upload_treinamento)
            
            # Exibir uma pré-visualização da planilha
            st.write("Pré-visualização dos dados carregados:")
            st.dataframe(trein.head())

            categorizar = st.button('Categorizar', key=3)

            if categorizar:
                try:
                    lista = bib.categorizador(palavras_categorizadas=cat[coluna].tolist(), treinamento=trein)

                    cat['categorias'] = lista

                    st.write("Dados categorizados:")
                    st.dataframe(cat)

                    # Adiciona botão para download
                    buffer = BytesIO()
                    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        cat.to_excel(writer, index=False, sheet_name='Categorizados')
                    
                    # Força os dados no buffer para uso no botão de download
                    buffer.seek(0)

                    st.download_button(
                        label="Baixar planilha categorizada",
                        data=buffer,
                        file_name="planilha_categorizada.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                except Exception as e:
                    st.error(f"Erro ao executar a categorização: {e}")

        except Exception as e:
            st.error(f"Erro ao carregar o arquivo: {e}")
