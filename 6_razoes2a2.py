"""
Lê o arquivo razoes_em_relacao_ao_Ne2_filtradas.csv e calcula a razão de cada linha em relação a todas debaixo dela (2 a 2, sem repetições) e salva tudo no arquivo todas_razoes_2a2_por_modelo.csv e também um arquivo para cada denominador, todos na pasta Razoes_2a2
"""

import pandas as pd
import os
from itertools import combinations

# Diretório dos dados
arquivo_dados = "razoes_em_relacao_ao_Ne2_filtradas.csv"
pasta_saida = os.path.join("./Razoes_2a2")
os.makedirs(pasta_saida, exist_ok=True)

# Lendo o arquivo principal
df = pd.read_csv(arquivo_dados)

# Separando colunas relevantes
colunas_modelos = [col for col in df.columns if col.startswith("Razao_Modelo")]

# Preparar DataFrame para armazenar os resultados gerais
resultados_geral = pd.DataFrame()

# Iterar sobre todas as combinações de linhas (íons) da tabela original
combinacoes_linhas = list(combinations(df.index, 2))  # Índices de todas as combinações possíveis

for idx1, idx2 in combinacoes_linhas:
    # Dados da linha denominador
    linha_denom = df.loc[idx1]
    ion_denom = linha_denom["Nome_Linha"]
    comp_denom = linha_denom["Comprimento_Linha"]

    # Dados da linha numerador
    linha_num = df.loc[idx2]
    ion_num = linha_num["Nome_Linha"]
    comp_num = linha_num["Comprimento_Linha"]

    # Preparar uma linha para o DataFrame de saída
    razoes_linhas = {
        "Ion_Denominador": ion_denom,
        "Comp_Denominador": comp_denom,
        "Ion_Numerador": ion_num,
        "Comp_Numerador": comp_num,
    }

    # Calcular razões para cada modelo
    for coluna_modelo in colunas_modelos:
        fluxo_denom = linha_denom[coluna_modelo]
        fluxo_num = linha_num[coluna_modelo]

        # Garantir que não haja divisão por zero
        if fluxo_denom != 0:
            razao = fluxo_num / fluxo_denom
        else:
            razao = None 

        # Adicionar a razão na linha com o nome do modelo
        razoes_linhas[coluna_modelo] = razao

    # Adicionar a linha ao DataFrame geral
    resultados_geral = pd.concat([resultados_geral, pd.DataFrame([razoes_linhas])], ignore_index=True)

# Salvar o arquivo geral com todas as razões calculadas
arquivo_geral = os.path.join(pasta_saida, "todas_razoes_2a2_por_modelo.csv")
resultados_geral.to_csv(arquivo_geral, index=False)
print(f"Arquivo geral salvo: {arquivo_geral}")

# Gerar arquivos separados para cada denominador
denominadores = resultados_geral[["Ion_Denominador", "Comp_Denominador"]].drop_duplicates()

for _, denominador in denominadores.iterrows():
    # Filtrar os dados para o denominador atual
    ion_denom = denominador["Ion_Denominador"]
    comp_denom = denominador["Comp_Denominador"]
    dados_denom = resultados_geral[
        (resultados_geral["Ion_Denominador"] == ion_denom) &
        (resultados_geral["Comp_Denominador"] == comp_denom)
    ]

    # Salvar em arquivo separado
    nome_arquivo = f"razoes_{ion_denom}_{comp_denom}.csv".replace(" ", "_")
    caminho_arquivo = os.path.join(pasta_saida, nome_arquivo)
    dados_denom.to_csv(caminho_arquivo, index=False)
    print(f"Arquivo separado salvo: {caminho_arquivo}")
