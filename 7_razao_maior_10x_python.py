""" Lê o arquivo 'todas_razoes_2a2_por_modelo.csv', faz a filtragem de apenas registrar as combinações de linhas que tenha um fator maior ou igual a 10 entre os valores máximo e mínimo global. Registra as que são maior que 10 no arquivo 'razoes_maior_10x.csv' na pasta raiz """ 

import pandas as pd
import os

# 1. Ler o arquivo 'todas_razoes_2a2_por_modelo.csv'
pasta_dados = "Razoes_2a2"
arquivo_dados = "todas_razoes_2a2_por_modelo.csv"
caminho_arquivo = os.path.join(pasta_dados, arquivo_dados)

print("Lendo o arquivo com todas as razões 2 a 2...")
df_razoes = pd.read_csv(caminho_arquivo) 
print("Arquivo lido com sucesso!")

# 2. Identificar as colunas das razões corretamente
colunas_razoes = [col for col in df_razoes.columns if col.startswith("Razao_Modelo")]

# 3. Converter valores para float
df_razoes[colunas_razoes] = df_razoes[colunas_razoes].apply(pd.to_numeric, errors='coerce')

# 4. Filtrar linhas com fator >= 10 entre o máximo e o mínimo
def fator_maior_10(linha):
    valores = linha[colunas_razoes].dropna()  # Ignorar valores ausentes
    if valores.empty:
        return False  # Se não há valores numéricos, ignorar linha
    max_valor = valores.max()
    min_valor = valores.min()
    fator = max_valor / min_valor if min_valor > 0 else 0  # Evitar divisão por zero
    return fator >= 10

df_filtrado = df_razoes[df_razoes.apply(fator_maior_10, axis=1)]

# 5. Salvar o novo arquivo apenas com as razões filtradas
arquivo_saida = os.path.join("./razoes_maior_10x.csv")
df_filtrado.to_csv(arquivo_saida, index=False)

print(f"Arquivo salvo corretamente em: {arquivo_saida}")

