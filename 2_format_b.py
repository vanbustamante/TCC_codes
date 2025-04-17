"""
Lê do arquivo _B.tab e entende que cada coluna é um dado (nome da linha, comprimento de onda e intensidade). Converte os comprimentos de onda para microns. Salva os dados (agora oficialmente 3 colunas) no _B_processado.csv
"""
import os

# Diretório raiz contendo as pastas dos modelos
diretorio_modelos = './Modelos'

# Função para processar o arquivo e salvar no formato CSV
def processar_arquivo(caminho_arquivo, caminho_saida):
    with open(caminho_arquivo, 'r') as f:
        linhas = f.readlines()
    
    # Abrindo o arquivo de saída no formato CSV
    with open(caminho_saida, 'w') as f_saida:
        # Escrevendo o cabeçalho
        f_saida.write("Nome,Comprimento_de_onda,Intensidade\n")
        
        # Processando as linhas de dados
        for linha in linhas:
            try:
                # Interpretando os valores com base na posição fixa
                nome = linha[0:15].strip()  # Nome da linha de emissão
                comprimento_onda = linha[16:29].strip()  # Comprimento de onda
                intensidade = linha[30:37].strip()  # Intensidade (log)
                
                # Validando os dados antes de processar
                if not comprimento_onda or not intensidade:
                    raise ValueError("Comprimento de onda ou intensidade ausente.")
                
                # Convertendo comprimento de onda para microns (se necessário)
                if comprimento_onda.endswith("A"):  # Comprimento de onda em Ångstrom
                    comprimento_onda = float(comprimento_onda[:-1]) * 1e-4  # De Å para microns
                elif comprimento_onda.endswith("m"):  # Já está em microns
                    comprimento_onda = float(comprimento_onda[:-1])
                else:
                    raise ValueError("Unidade desconhecida no comprimento de onda.")
                
                # Mantendo a intensidade como string para evitar alterações
                intensidade = float(intensidade)  # Converte para número para validar
                intensidade_str = f"{intensidade:.3f}"  # Formata com 3 casas decimais

                # Gravando no arquivo CSV
                f_saida.write(f"{nome},{comprimento_onda:.6f},{intensidade_str}\n")

            except ValueError as e:
                # Informar o erro ao processar a linha, mas continuar o processamento
                print(f"Erro ao processar linha: '{linha.strip()}' - {e}")
            except IndexError:
                # Captura problemas de formatação inesperados
                print(f"Erro de índice ao processar linha: '{linha.strip()}'")

# Percorre as pastas do diretório e processa os arquivos
for raiz, _, arquivos in os.walk(diretorio_modelos):
    for arquivo in arquivos:
        if arquivo.endswith('_B.tab'):
            caminho_arquivo = os.path.join(raiz, arquivo)
            caminho_saida = caminho_arquivo.replace('_B.tab', '_B_processado.csv')
            print(f"Processando arquivo: {caminho_arquivo}")
            processar_arquivo(caminho_arquivo, caminho_saida)
print("Processamento concluído!")

