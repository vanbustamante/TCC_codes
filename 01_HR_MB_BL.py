import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import LogLocator, LogFormatterMathtext

# Caminhos para as pastas
caminho_MB2016 = './MB2016'
caminho_BL1995 = './BL1995'

# Função para carregar dados MB2016
def carregar_dados_MB2016(filename):
    data = np.loadtxt(os.path.join(caminho_MB2016, filename), skiprows=1, usecols=(0, 1, 2, 3))
    M_inicial, M_final, log_T_eff, log_L = data[:, 0], data[:, 1], data[:, 2], data[:, 3]
    return M_inicial[0], M_final, log_T_eff, log_L

# Função para carregar dados BL1995
def carregar_dados_BL1995(filename):
    data = np.loadtxt(os.path.join(caminho_BL1995, filename), skiprows=1, usecols=(0, 1, 2, 3))
    M_inicial, M_final, log_T_eff, log_L = data[:, 0], data[:, 1], data[:, 2], data[:, 3]
    return M_inicial[0], M_final, log_T_eff, log_L

# Função para carregar dados do grid
def carregar_dados_grid(filename):
    data = np.loadtxt(filename, skiprows=1, usecols=(0, 2, 3))  # Lê M_inicial, log_T_eff, log_L
    M_inicial, log_T_eff, log_L = data[:, 0], data[:, 1], data[:, 2]
    return M_inicial, log_T_eff, log_L

# Carregar os dados MB2016
M_inicial_Z0100MI1, M_final_Z0100MI1, log_T_eff_Z0100MI1, log_L_Z0100MI1 = carregar_dados_MB2016('Z0100MI1.txt')
M_inicial_Z0100MI3, M_final_Z0100MI3, log_T_eff_Z0100MI3, log_L_Z0100MI3 = carregar_dados_MB2016('Z0100MI3.txt')
M_inicial_Z0200MI1, M_final_Z0200MI1, log_T_eff_Z0200MI1, log_L_Z0200MI1 = carregar_dados_MB2016('Z0200MI1.txt')
M_inicial_Z0200MI3, M_final_Z0200MI3, log_T_eff_Z0200MI3, log_L_Z0200MI3 = carregar_dados_MB2016('Z0200MI3.txt')

# Carregar os dados BL1995
M_inicial_MI3MF0p625, M_final_MI3MF0p625, log_T_eff_MI3MF0p625, log_L_MI3MF0p625 = carregar_dados_BL1995('MI3MF0p625.txt')
M_inicial_MI5MF0p836, M_final_MI5MF0p836, log_T_eff_MI5MF0p836, log_L_MI5MF0p836 = carregar_dados_BL1995('MI5MF0p836.txt')
M_inicial_MI7MF0p940, M_final_MI7MF0p940, log_T_eff_MI7MF0p940, log_L_MI7MF0p940 = carregar_dados_BL1995('MI7MF0p940.txt')

# Carregar os dados do grid
M_inicial_grid, log_T_eff_grid, log_L_grid = carregar_dados_grid('grid32.txt')

# Transformar log(T_eff) e log(L) em valores reais
T_eff_Z0100MI1 = 10 ** log_T_eff_Z0100MI1
L_Z0100MI1 = 10 ** log_L_Z0100MI1

T_eff_Z0200MI1 = 10 ** log_T_eff_Z0200MI1
L_Z0200MI1 = 10 ** log_L_Z0200MI1

T_eff_Z0100MI3 = 10 ** log_T_eff_Z0100MI3
L_Z0100MI3 = 10 ** log_L_Z0100MI3

T_eff_Z0200MI3 = 10 ** log_T_eff_Z0200MI3
L_Z0200MI3 = 10 ** log_L_Z0200MI3

T_eff_MI3MF0p625 = 10 ** log_T_eff_MI3MF0p625
L_MI3MF0p625 = 10 ** log_L_MI3MF0p625

T_eff_MI5MF0p836 = 10 ** log_T_eff_MI5MF0p836
L_MI5MF0p836 = 10 ** log_L_MI5MF0p836

T_eff_MI7MF0p940 = 10 ** log_T_eff_MI7MF0p940
L_MI7MF0p940 = 10 ** log_L_MI7MF0p940

# Transformar os pontos do grid
T_eff_grid = 10 ** log_T_eff_grid
L_grid = 10 ** log_L_grid

## Criar a figura
plt.figure(figsize=(12, 8))

# Plotar as curvas MB2016
plt.plot(T_eff_Z0100MI1, L_Z0100MI1, color='blue', linestyle='--', label=f'{M_inicial_Z0100MI1} M☉ (MB)', linewidth=1.5)
plt.plot(T_eff_Z0200MI1, L_Z0200MI1, color='red', linestyle='-', label=f'{M_inicial_Z0200MI1} M☉ (MB)', linewidth=1.5)
plt.plot(T_eff_Z0100MI3, L_Z0100MI3, color='orange', linestyle='--', label=f'{M_inicial_Z0100MI3} M☉ (MB)', linewidth=1.5)
plt.plot(T_eff_Z0200MI3, L_Z0200MI3, color='green', linestyle='-', label=f'{M_inicial_Z0200MI3} M☉ (MB)', linewidth=1.5)

# Plotar as curvas BL1995
plt.plot(T_eff_MI3MF0p625, L_MI3MF0p625, color='brown', linestyle='--', label=f'{M_inicial_MI3MF0p625} M☉ (BL)', linewidth=1.5)
plt.plot(T_eff_MI5MF0p836, L_MI5MF0p836, color='purple', linestyle='-', label=f'{M_inicial_MI5MF0p836} M☉ (BL)', linewidth=1.5)
plt.plot(T_eff_MI7MF0p940, L_MI7MF0p940, color='olive', linestyle='-', label=f'{M_inicial_MI7MF0p940} M☉ (BL)', linewidth=1.5)

# Plotar os pontos do grid
plt.scatter(T_eff_grid, L_grid, color='black', marker='*', s=100, label='Pontos do Grid', zorder=5)

# Configurações do gráfico
plt.xlabel(r'T$_{\mathrm{eff}}$ (K)', fontsize=18)
plt.ylabel(r'Luminosidade (L/L$_\odot$)', fontsize=18)
plt.xscale('log')
plt.yscale('log')

ax = plt.gca()

# Definir os valores específicos de temperatura para os ticks
x_ticks_values = [30000, 50000, 75000, 150000, 250000, 390000]

# Formatar os valores com separação de milhar (usando ponto)
x_ticks_labels_formatted = [f"{label:,}".replace(",", ".") for label in x_ticks_values]

# Definir os ticks e labels
plt.xticks([10**(4.477), 10**(4.699), 10**(4.875), 10**(5.176), 10**(5.397), 10**(5.591)], 
           labels=x_ticks_labels_formatted, fontsize=14)
plt.yticks(fontsize=14)

# Grade e limites
plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
plt.xlim(10**5.75, 10**4.25)
plt.ylim(10**1.5, 10**5.0)

# Legenda e salvar
plt.legend(loc='lower right', fontsize=14, frameon=True)
plt.tight_layout()
plt.savefig('curvas_formatadas.png', dpi=300)

