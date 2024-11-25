import streamlit as st
import pandas as pd
import biblioteca as bib
from io import BytesIO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import os

def categorizador(palavras_categorizadas, treinamento):
    # Criar uma lista para armazenar as palavras e categorias do treinamento
    palavras_treinamento = []
    categorias = []
    
    # Iterar pelas linhas do dataframe de treinamento
    for _, row in treinamento.iterrows():
        categoria = row.iloc[0]  # Primeira coluna é a categoria
        palavras_chave = row.iloc[1:].dropna().values  # As colunas seguintes são palavras-chave
        
        # Adicionar cada palavra-chave à lista de palavras e associar à categoria
        for palavra in palavras_chave:
            palavras_treinamento.append(palavra)
            categorias.append(categoria)

    # Criar um modelo de classificação usando TF-IDF + Regressão Logística
    model = make_pipeline(TfidfVectorizer(), LogisticRegression())
    
    # Treinar o modelo com as palavras-chave e suas categorias
    model.fit(palavras_treinamento, categorias)
    
    # Prever as categorias das palavras fornecidas
    categorias_preditas = model.predict(palavras_categorizadas)
    
    return categorias_preditas

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
                    lista = categorizador(palavras_categorizadas=cat[coluna].tolist(), treinamento=trein)

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
