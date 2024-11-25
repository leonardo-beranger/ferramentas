import pandas as pd
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

# Função para consolidar arquivos Excel de um diretório
def consolidar_excel(diretorio):
    arquivos_excel = [f for f in os.listdir(diretorio) if f.endswith('.xlsx') or f.endswith('.xls')]
    dfs = []

    for arquivo in arquivos_excel:
        caminho_arquivo = os.path.join(diretorio, arquivo)
        df = pd.read_excel(caminho_arquivo)
        dfs.append(df)

    # Concatenando todos os dataframes em um único
    df_consolidado = pd.concat(dfs, ignore_index=True)

    # Resetando o índice e descartando o índice anterior como coluna
    df_consolidado = df_consolidado.reset_index(drop=True)
    
    return df_consolidado