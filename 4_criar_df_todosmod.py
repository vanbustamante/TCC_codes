"""
Lê os arquivos _IR27.csv de cada modelo e junta tudo num dataframe salvo em dados_combinados_IR27.csv na pasta raiz.
"""

import pandas as pd
import glob
import os

# Diretório principal onde estão os modelos
path = "./Modelos/"  # Ajuste o caminho conforme sua estrutura

# Encontra todos os arquivos *_IR27.csv nas subpastas
sources_list = glob.glob(os.path.join(path, "*/*_IR27.csv"))

# Inicializa o dataframe final vazio
df_final = pd.DataFrame()

# Processa cada arquivo e adiciona os dados ao dataframe final
for arq in sources_list:
    try:
        # Lê o arquivo filtrado
        df = pd.read_csv(arq)

        # Verifica duplicatas no par Nome + Comprimento_de_onda
        duplicatas = df[df.duplicated(subset=['Nome', 'Comprimento_de_onda'], keep=False)]
        if not duplicatas.empty:
            print(f"Atenção: Duplicatas encontradas em {arq}.")
            print("Linhas duplicadas (primeiras 5 exibidas):")
            print(duplicatas.head())  # Exibe até 5 duplicatas no terminal para análise
            # REMOVE TODAS AS DUPLICATAS
            df = df[~df.duplicated(subset=['Nome', 'Comprimento_de_onda'], keep=False)]
            print(f"{len(duplicatas)} linhas duplicadas removidas.")

        # Cria uma coluna identificadora do modelo com base no nome do arquivo
        nome_modelo = os.path.basename(arq).replace("_IR27.csv", "")  # Nome do modelo
        df['Modelo'] = nome_modelo

        # Reorganiza as colunas (Nome, Comprimento_de_onda, Intensidade, Modelo)
        df = df[['Nome', 'Comprimento_de_onda', 'Intensidade', 'Modelo']]

        # Junta no dataframe final usando Nome + Comprimento_de_onda como chave
        if df_final.empty:
            # Para o primeiro arquivo, inicializa o dataframe
            df_final = df.pivot(index=['Nome', 'Comprimento_de_onda'], columns='Modelo', values='Intensidade')
        else:
            # Para os arquivos subsequentes, faz o merge com o dataframe existente
            df_temp = df.pivot(index=['Nome', 'Comprimento_de_onda'], columns='Modelo', values='Intensidade')
            df_final = pd.merge(df_final, df_temp, on=['Nome', 'Comprimento_de_onda'], how='outer')

    except Exception as e:
        print(f"Erro ao processar o arquivo {arq}: {e}")

# Após o loop, reseta o índice para facilitar a visualização e exportação
df_final.reset_index(inplace=True)

# Salva o dataframe combinado em um arquivo CSV na pasta raiz
output_path = os.path.join("./dados_combinados_IR27.csv")
df_final.to_csv(output_path, index=False, na_rep='NaN')  # Salva NaN para valores ausentes
print(f"Dados combinados salvos em: {output_path}")

# Estatísticas gerais sobre o arquivo combinado
num_modelos = len(df_final.columns) - 2  # Colunas menos as duas iniciais (Nome e Comprimento_de_onda)
num_linhas = len(df_final)  # Total de linhas
print(f"Total de modelos (colunas de intensidade): {num_modelos}")
print(f"Total de linhas (linhas de emissão únicas): {num_linhas}")
print("Visualização das primeiras linhas do dataframe final:")
print(df_final.head())

