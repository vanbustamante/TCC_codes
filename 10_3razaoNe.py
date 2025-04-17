import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from matplotlib.ticker import FuncFormatter

# Arquivo de dados
arquivo_dados = "razoes_maior_10x.csv"

# Configuração global do Matplotlib para usar LaTeX
plt.rcParams['text.usetex'] = True
plt.rcParams['font.size'] = 20
plt.rcParams['axes.labelsize'] = 22
plt.rcParams['axes.titlesize'] = 22
plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['ytick.labelsize'] = 18

# Leitura do CSV
df_razoes = pd.read_csv(arquivo_dados)
colunas_modelos = [col for col in df_razoes.columns if col.startswith("Razao_Modelo")]

# Criação do DataFrame com Informações dos Modelos
modelos_info = []
for coluna in colunas_modelos:
    try:
        # Extrair as informações da coluna
        _, _, hden, luminosidade_log, temperatura_log, massa_inicial, massa_final = coluna.split("_")
        
        # Calcular luminosidade
        luminosidade_erg = 10 ** float(luminosidade_log)  
        temperatura = 10 ** float(temperatura_log)  
        luminosidade = luminosidade_erg / 3.826e33

        # Adicionar as informações ao modelo
        modelos_info.append({
            "coluna": coluna,
            "hden": float(hden),
            "luminosidade": luminosidade,
            "temperatura": temperatura,
            "massa_inicial": float(massa_inicial),
            "massa_final": float(massa_final)
        })
    except ValueError as e:
        print(f"Erro ao processar a coluna {coluna}: {e}")

# Criação do DataFrame df_modelos
df_modelos = pd.DataFrame(modelos_info)

# Verifique se o df_modelos foi criado corretamente
print(df_modelos.head())

# Criar pasta para salvar gráficos
pasta_graficos = "Plots_Comparacao_Obs"
os.makedirs(pasta_graficos, exist_ok=True)

# Função para formatar íons
def formatar_ion(ion):
    numeros_romanos = {"1": "I", "2": "II", "3": "III", "4": "IV", "5": "V", "6": "VI"}
    if ion == "H2":
        return "H$_2$"
    partes = ion.split(" ")
    if len(partes) == 2:
        elemento, estado = partes
        estado_romano = numeros_romanos.get(estado, estado)
        return f"[{elemento} {estado_romano}]"
    return ion

# Dados de observação para faixas no gráfico (do jeito que você descreveu)
observacoes = {
    "[Ne VI] 7.64318 $\mu$m / [Ne III] 15.5509 $\mu$m": [
        {"NP": "PN K 4-16", "razao": 0.0500, "erro": 0.0300},
        {"NP": "PN M 3-50", "razao": 0.1100, "erro": 0.0400},
        {"NP": "PN K 3-56", "razao": 0.1800, "erro": 0.1100},
        {"NP": "PN Pe 2-7", "razao": 0.0310, "erro": 0.0100},
        {"NP": "WRAY 15-1585", "razao": 0.3210, "erro": 0.0280}
    ],
    "[Ne VI] 7.64318 $\mu$m / [Ne V] 14.3228 $\mu$m": [
        {"NP": "PN K 4-16", "razao": 0.1900, "erro": 0.1300},
        {"NP": "PN M 3-50", "razao": 0.0310, "erro": 0.0120},
        {"NP": "PN K 3-56", "razao": 0.1700, "erro": 0.1000},
        {"NP": "PN Pe 2-7", "razao": 0.0100, "erro": 0.0030},
        {"NP": "WRAY 15-1585", "razao": 0.1620, "erro": 0.0140}
    ],
    "[Ne VI] 7.64318 $\mu$m / [Ne V] 24.2065 $\mu$m": [
        {"NP": "PN K 4-16", "razao": 0.4000, "erro": 0.3000},
        {"NP": "PN M 3-50", "razao": 0.0160, "erro": 0.0060},
        {"NP": "PN K 3-56", "razao": 0.2100, "erro": 0.1300},
        {"NP": "PN Pe 2-7", "razao": 0.0110, "erro": 0.0040},
        {"NP": "WRAY 15-1585", "razao": 0.2310, "erro": 0.0200}
    ]
}

# Filtrar apenas as razões específicas de [Ne VI]
for index, linha in df_razoes.iterrows():
    numerador = linha["Ion_Numerador"]
    denominador = linha["Ion_Denominador"]
    comp_denominador = linha["Comp_Denominador"]
    
    # Filtrar razões específicas de [Ne VI] 7.64318 / [Ne III] 15.5509, [Ne VI] 7.64318 / [Ne V] 14.3228 e [Ne VI] 7.64318 / [Ne V] 24.2065
    if (numerador == "Ne 6" and denominador == "Ne 3" and comp_denominador == 15.5509) or \
       (numerador == "Ne 6" and denominador == "Ne 5" and comp_denominador == 14.3228) or \
       (numerador == "Ne 6" and denominador == "Ne 5" and comp_denominador == 24.2065) :
        
        comp_numerador = linha["Comp_Numerador"]
        dados_filtro = linha[colunas_modelos]

        massas_iniciais = []
        temperaturas = []
        razoes = []
        tamanhos_pontos = []

        for _, modelo in df_modelos.iterrows():
            coluna = modelo["coluna"]
            massa_inicial = modelo["massa_inicial"]
            temperatura = modelo["temperatura"]

            if coluna in dados_filtro.index:
                massas_iniciais.append(massa_inicial)
                temperaturas.append(temperatura)
                razoes.append(dados_filtro[coluna])
                tamanho_ponto = (modelo["hden"] - df_modelos["hden"].min()) / (df_modelos["hden"].max() - df_modelos["hden"].min()) * 100 + 20
                tamanhos_pontos.append(tamanho_ponto)

        # Verificar se há dados para plotar
        if not massas_iniciais:
            print(f"Nenhum dado para a razão {numerador} / {denominador}")
            continue

        # Plotagem do gráfico
        print(f"Gerando gráfico para {numerador} / {denominador}")  # Verificando se estamos gerando o gráfico corretamente
        plt.figure(figsize=(10, 6))
        titulo = (f"{formatar_ion(numerador)} {comp_numerador} $\mu$m / {formatar_ion(denominador)} {comp_denominador} $\mu$m")
        plt.title(titulo, fontsize=14)
        plt.xlabel(r"M$_{SP}$ (M$_\odot$)", fontweight='bold')
        plt.ylabel(r"RAZÃO DE LINHAS", fontweight='bold')
        plt.yscale('log')
        plt.grid(True)

        if massas_iniciais:
            scatter = plt.scatter(
                x=massas_iniciais,
                y=razoes,
                c=temperaturas,
                cmap="viridis",
                alpha=0.7,
                s=tamanhos_pontos
            )
            cbar = plt.colorbar(scatter)
            cbar.set_label(r"TEMPERATURA DA ESTRELA CENTRAL (10$^3$ K)", fontsize=16, fontweight='bold')
            cbar.set_ticks([50000, 100000, 150000, 200000, 250000, 300000, 350000, 400000])
            cbar.set_ticklabels(["50", "100", "150", "200", "250", "300", "350", "400"])

        # Adicionar faixas de observação
        if titulo in observacoes:
            for observacao in observacoes[titulo]:
                nome_NP = observacao["NP"]
                razao = observacao["razao"]
                erro = observacao["erro"]
                plt.fill_between(
                    [7.1, razao], razao - erro, razao + erro,
                    alpha=0.2, label=nome_NP
                )
                #plt.plot([7.1, razao], [razao, razao], linestyle='--', linewidth=2, color='gray', alpha=0.7)
                
        # Exibir a legenda
        plt.legend(loc="lower right", fontsize=10)

        # Verificar se as faixas de observação estão sendo adicionadas
        if titulo in observacoes:
            print(f"Faixas de observação adicionadas para {titulo}")
        else:
            print(f"Nenhuma faixa de observação para {titulo}")

        # Ajuste automático dos ticks do eixo Y
        def formatador_y(value, _):
            if value == 10**0:
                return "1"
            elif value == 10**1:
                return "10"
            else:
                return f"$10^{{{int(np.log10(value))}}}$"
        plt.gca().yaxis.set_major_formatter(FuncFormatter(formatador_y))

        # Garantir apenas 1, 3, 5, 7 no eixo X
        plt.xticks([1, 3, 5, 7])

        # Ajustar layout para não cortar a legenda
        plt.tight_layout()

        # Salvar gráfico
        nome_arquivo = (f"{numerador}_{comp_numerador}_div_{denominador}_{comp_denominador}.jpg").replace(" ", "_").replace("{", "").replace("}", "")
        caminho_grafico = os.path.join(pasta_graficos, nome_arquivo)
        plt.savefig(caminho_grafico, format="jpg", dpi=300)
        plt.close()

