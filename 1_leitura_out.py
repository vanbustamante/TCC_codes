"""
Leitura dos arquivos .out, pegando as "Emergent line intensities", que inicialmente estão dispostas em 3 'grandes' colunas, e transformando em um arquivo (_B.tab) com apenas uma 'grande' coluna, com as informações de nome, comprimento de onda e intensidade (sem cabeçalho)
"""

import os
import pandas as pd
import glob

#========================================
# Função que extrai a tabela de fluxos de linhas do arquivo de saída do Cloudy
def extrai_tabela(filecloudy, file_3cols):
    with open(filecloudy) as infile, open(file_3cols, 'w') as outfile:
        copiar = False
        for linha in infile:
            if linha.strip() == "Emergent line intensities":
                copiar = True
            elif linha.strip() == "":
                copiar = False
            elif copiar:
                outfile.write(linha)

#========================================
# Função que transforma a tabela de 3 colunas em uma única coluna
def transforma_uma_coluna(file_3cols, file_1col):
    lins_revi = pd.read_fwf(
        file_3cols,
        colspecs=[(0, 37), (53, 90), (106, 143)],
        header=None,
        names=["a", "b", "c"],
        converters={"a": str, "b": str, "c": str},
        skip_blank_lines=True
    )
    with open(file_1col, 'w') as ofile:
        for coluna in ["a", "b", "c"]:
            for linha in lins_revi[coluna]:
                if not pd.isna(linha) and ".." not in linha:
                    ofile.write(linha + "\n")

#========================================
# Função que lê e retorna os dados em formato tabular
def le_dados(file_1col):
    dados = pd.read_fwf(
        file_1col,
        colspecs=[(0, 9), (10, 16), (17, 18), (20, 26)],
        header=None,
        names=["line", "wave", "range", "flux"],
        skip_blank_lines=True
    )
    return dados

#========================================
# Rotina principal
#========================================

def processa_modelos(diretorio):
    # Caminho para os arquivos de saída do Cloudy
    arquivos = glob.glob(os.path.join(diretorio, "*/*.out"))
    print(f"Quantidade de arquivos encontrados: {len(arquivos)}")

    for arquivo in arquivos:
        print(f"Processando: {arquivo}")
        # Arquivo intermediário com 3 colunas
        file_3cols = arquivo.replace(".out", ".tab")
        extrai_tabela(arquivo, file_3cols)

        # Arquivo intermediário com 1 coluna
        file_1col = arquivo.replace(".out", "_B.tab")
        transforma_uma_coluna(file_3cols, file_1col)

        # Lê os dados do arquivo transformado
        dados = le_dados(file_1col)


    print("Processamento concluído!")

#========================================
# Execução
#========================================
if __name__ == "__main__":
    diretorio_modelos = "./Modelos/"
    processa_modelos(diretorio_modelos)

