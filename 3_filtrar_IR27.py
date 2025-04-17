"""
Lê _B_processado.csv, remove as linhas desnecessárias (PAHC, PAH, NIR, MIR, NMIR, F12, F25, MIPS, IRAC, SX, etc), filtra os dados para o comprimento de onda entre 5.5 e 27 microns, salva em _IR27.csv.
"""
import pandas as pd
import glob
import os

# Diretorio principal onde estão os modelos
path = "./Modelos/"

# Encontra todos os arquivos *_B_processado.csv nas subpastas
sources_list = glob.glob(os.path.join(path, "*/*_B_processado.csv"))

# Verifica quantidade de arquivos lidos
numarq = len(sources_list)
print(f"Quantidade de arquivos lidos: {numarq}")

# Percorre cada arquivo de modelo
for arq in sources_list:
    try:
        # Lê o arquivo
        df = pd.read_csv(arq)

        # Exibe as primeiras linhas para verificar o arquivo
        print(f"Arquivo lido com sucesso: {arq}")
        print("Primeiras linhas do arquivo:")
        print(df.head())

        # Remove as linhas desnecessárias (índice 1 a 42)
        df = df.drop(index=range(1, 43), errors='ignore')

        # Converte a coluna 'Intensidade' para numérico
        df['Intensidade'] = pd.to_numeric(df['Intensidade'], errors='coerce')

        # Filtra os dados para o comprimento de onda entre 5.5 e 27 microns
        df_filtrado = df[(df['Comprimento_de_onda'] >= 5.5) & (df['Comprimento_de_onda'] <= 27)]

        # Verifica os dados após o filtro
        print("Dados filtrados:")
        print(df_filtrado.head())

        # Cria o caminho para o arquivo de saída
        output_path = arq.replace("_B_processado.csv", "_IR27.csv")

        # Salva o arquivo filtrado
        df_filtrado.to_csv(output_path, index=False)
        print(f"Arquivo filtrado salvo com sucesso: {output_path}")

    except Exception as e:
        print(f"Erro ao processar o arquivo {arq}: {e}")

print("Processamento finalizado!")

