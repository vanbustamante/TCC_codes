import pandas as pd
import os

# 1. Ler o arquivo com as razões
arquivo_dados = "razoes_maior_10x.csv"
df_razoes = pd.read_csv(arquivo_dados)

# 2. Identificar colunas dos modelos
colunas_modelos = [col for col in df_razoes.columns if col.startswith("Razao_Modelo")]

# 3. Estrutura para armazenar resultados
resultados = []
variacoes = []

# 4. Iterar sobre cada combinação de razão individual
combinacoes_razoes = df_razoes.groupby(["Ion_Numerador", "Comp_Numerador", "Ion_Denominador", "Comp_Denominador"])

for (numerador, comp_num, denominador, comp_den), grupo in combinacoes_razoes:
    dados_por_massa = {}
    
    for coluna in colunas_modelos:
        _, _, hden, luminosidade, temperatura, massa_inicial, massa_final = coluna.split("_")
        massa_inicial = float(massa_inicial)
        
        valores_razao = grupo[coluna].dropna()
        if not valores_razao.empty:
            if massa_inicial not in dados_por_massa:
                dados_por_massa[massa_inicial] = []
            dados_por_massa[massa_inicial].extend(valores_razao.tolist())
    
    estatisticas_massa = {}
    for massa_inicial, valores_razao in dados_por_massa.items():
        valores_razao = pd.Series(valores_razao)
        
        minimo = valores_razao.min()
        maximo = valores_razao.max()
        media = valores_razao.mean()
        mediana = valores_razao.median()
        desvio_padrao = valores_razao.std()
        intervalo = maximo - minimo
        
        estatisticas_massa[massa_inicial] = {
            "Minimo": minimo,
            "Maximo": maximo,
            "Media": media,
            "Mediana": mediana,
            "Desvio_Padrao": desvio_padrao,
            "Intervalo": intervalo,
            "N_Dados": len(valores_razao)
        }
        
        resultados.append({
            "Ion_Numerador": numerador,
            "Lambda_Numerador": comp_num,
            "Ion_Denominador": denominador,
            "Lambda_Denominador": comp_den,
            "Massa_Inicial": massa_inicial,
            "Minimo": minimo,
            "Maximo": maximo,
            "Media": media,
            "Mediana": mediana,
            "Desvio_Padrao": desvio_padrao,
            "Intervalo": intervalo,
            "N_Dados": len(valores_razao)
        })
    
    if len(estatisticas_massa) >= 2:
        massas_disponiveis = sorted(estatisticas_massa.keys())
        valores_min = [estatisticas_massa[m]["Minimo"] for m in massas_disponiveis]
        valores_max = [estatisticas_massa[m]["Maximo"] for m in massas_disponiveis]
        
        variacao_total = max(valores_max) - min(valores_min)
        variacao_relativa = variacao_total / max(valores_max) if max(valores_max) != 0 else 0
        
        variacoes.append({
            "Ion_Numerador": numerador,
            "Lambda_Numerador": comp_num,
            "Ion_Denominador": denominador,
            "Lambda_Denominador": comp_den,
            "Variacao_Total": variacao_total,
            "Variacao_Relativa": variacao_relativa
        })
    
    if 1.0 in estatisticas_massa and 7.0 in estatisticas_massa:
        max_1 = estatisticas_massa[1.0]["Maximo"]
        max_7 = estatisticas_massa[7.0]["Maximo"]
        diferenca_maximos = abs(max_1 - max_7)
        variacoes.append({
            "Ion_Numerador": numerador,
            "Lambda_Numerador": comp_num,
            "Ion_Denominador": denominador,
            "Lambda_Denominador": comp_den,
            "Diferenca_Max_1_7": diferenca_maximos
        })

# 5. Salvar resultados
pasta_dados = "Análises"
os.makedirs(pasta_dados, exist_ok=True)

arquivo_estatisticas = os.path.join(pasta_dados, "estatisticas_razoes_por_massa.csv")
df_resultados = pd.DataFrame(resultados)
df_resultados.to_csv(arquivo_estatisticas, index=False)

arquivo_variacoes = os.path.join(pasta_dados, "variacoes_razoes.csv")
df_variacoes = pd.DataFrame(variacoes)
df_variacoes.to_csv(arquivo_variacoes, index=False)

print(f"Estatísticas salvas em: {arquivo_estatisticas}")
print(f"Variações salvas em: {arquivo_variacoes}")

