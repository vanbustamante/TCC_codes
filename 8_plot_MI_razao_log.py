"""
Lê o arquivo razoes_maior_10x.csv, retira as informações de cada modelo (cada coluna) de massa inicial, hden, temperatura, etc. Gera os gráficos de razões por massa inicial para cada combinação de linhas. Salva os gráficos dentro da pasta Plots_MI_Razoes_log.
"""
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
    _, _, hden, luminosidade_log, temperatura_log, massa_inicial, massa_final = coluna.split("_")
    luminosidade_erg = 10 ** float(luminosidade_log)  
    temperatura = 10 ** float(temperatura_log)  
    luminosidade = luminosidade_erg / 3.826e33
    modelos_info.append({
        "coluna": coluna,
        "hden": float(hden),
        "luminosidade": luminosidade,
        "temperatura": temperatura,
        "massa_inicial": float(massa_inicial),
        "massa_final": float(massa_final)
    })
df_modelos = pd.DataFrame(modelos_info)

# Criar pasta para salvar gráficos
pasta_graficos = "Plots_MI_Razoes_log_2"
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

# Loop para criação dos gráficos
for index, linha in df_razoes.iterrows():
    numerador = linha["Ion_Numerador"]
    denominador = linha["Ion_Denominador"]
    comp_numerador = linha["Comp_Numerador"]
    comp_denominador = linha["Comp_Denominador"]
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

    plt.figure(figsize=(10, 6))
    titulo = (f"{formatar_ion(numerador)} ({comp_numerador} $\mu$m) / {formatar_ion(denominador)} ({comp_denominador} $\mu$m)")
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

    # Ajuste automático dos ticks do eixo Y para valores mais legíveis
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
    
    # Criar legenda para tamanhos dos pontos
    hden_exemplos = [2, 3, 4]  # Exemplos para legenda
    tamanhos_legenda = [(h - df_modelos["hden"].min()) / (df_modelos["hden"].max() - df_modelos["hden"].min()) * 100 + 20 for h in hden_exemplos]

    # Cor roxa baseada no colormap viridis
    cor_legenda = plt.get_cmap("viridis")(0.1)

    legenda_tamanhos = [
        plt.scatter([], [], s=tam, color=cor_legenda, alpha=0.7, edgecolors="black", linewidth=0.5, label=f"hden {h}")
        for h, tam in zip(hden_exemplos, tamanhos_legenda)
    ]

    # Posicionar a legenda dentro do gráfico entre massas 1 e 3
    plt.legend(handles=legenda_tamanhos, loc='upper left', bbox_to_anchor=(0.1, 0.25), frameon=True, fontsize=14)

    # Ajustar layout para não cortar a legenda
    plt.tight_layout()

    # Salvar gráfico
    nome_arquivo = (f"{numerador}_{comp_numerador}_div_{denominador}_{comp_denominador}.jpg").replace(" ", "_").replace("{", "").replace("}", "")
    caminho_grafico = os.path.join(pasta_graficos, nome_arquivo)
    plt.savefig(caminho_grafico, format="jpg", dpi=300) 
    plt.close()

