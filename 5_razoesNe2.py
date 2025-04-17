"""
Lê o arquivo dados_combinados_IR27.csv, transforma as intensidades a valor sem logaritmo, faz a razão de cada linha pelo Ne II (12.8101) e salva as razões que tiverem em ao menos um dos modelos um valor maior que 0.01 no arquivo razoes_em_relacao_ao_Ne2_filtradas.csv na pasta raiz
"""
import os
import pandas as pd

# 1) Carregar os dados originais
arquivo_original = "dados_combinados_IR27.csv"
df = pd.read_csv(arquivo_original)

# 2) Obter as colunas dos modelos (intensidades em log)
colunas_modelos = [col for col in df.columns if 'Modelo' in col]

# 3) Transformar as intensidades logarítmicas em valores reais (10^log)
df_intensidades = df.copy()  # Copiar o dataframe original
for col in colunas_modelos:
    df_intensidades[col] = 10 ** df[col]

# 4) Filtrar a linha referente ao Ne II (12.8101)
linha_ne2 = df_intensidades[df_intensidades['Comprimento_de_onda'] == 12.8101]
if linha_ne2.empty:
    raise ValueError("Linha de [Ne II] (12.8101) não encontrada no arquivo.")

# Intensidades da linha de [Ne II]
intensidades_ne2 = linha_ne2.iloc[0][colunas_modelos]  # Seleciona a primeira ocorrência

# 5) Calcular razões em relação ao [Ne II] para todas as outras linhas
razoes_relevantes = []  # Lista acumulativa para guardar as razões relevantes
for idx, linha in df_intensidades.iterrows():
    nome_linha = linha['Nome']
    comprimento_onda = linha['Comprimento_de_onda']
    intensidades_linha = linha[colunas_modelos]

    # Calcular razões
    razoes = intensidades_linha / intensidades_ne2

    # Verificar se a razão máxima é > 0.01
    if razoes.max() > 0.01:
        razoes_relevantes.append({
            'Nome_Linha': nome_linha,
            'Comprimento_Linha': comprimento_onda,
            **{f'Razao_{modelo}': razoes[modelo] for modelo in colunas_modelos}
        })


# 7) Salvar resultados no arquivo CSV
arquivo_saida =  os.path.join("./razoes_em_relacao_ao_Ne2_filtradas.csv")
pd.DataFrame(razoes_relevantes).to_csv(arquivo_saida, index=False)

print(f"Processamento concluído! Resultados salvos em: {arquivo_saida}")

