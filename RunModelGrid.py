#===============================================================
# Model Grid
# Set 2020
# by Isabel Aleman
#===============================================================

import numpy as np
import matplotlib.pyplot as plt
import os
import pyCloudy as pc

print(' ')
print('Starting ...')
print(' ')

#===============================================================
# We define a function that will manage the input files of Cloudy. 
# This allow to easily change some parameters, very usefull to do a grid.
def make_model(dir_, model_name, T, L, dens):

    t3 = T / 1000.
    full_model_name = f'{model_name}_{dens}_{L:.0f}_{t3:.0f}'


    emis_tab = ['H  1  4861.33A',
            'H  1  6562.81A',
            'H  1  4340.46A',
            'H  1  2.16551m',
            'H  1  7.45777m',
            'H  1  12.3684m',
            'H  1  7.50038m',
            'H  1  19.0565m',
            'H  1  11.3055m',
            'H  1  27.7955m',
            'He 1  5875.64A',
            'Ca B  5875.64A',
            'He 1  4471.49A',
            'Ca B  4471.49A',
            'He 1  5015.68A',
            'He 1  6678.15A',
            'He 1  7065.22A',
            'He 2  4685.64A',
            'He 2  7.37993m',
            'He 1  7.38026m',
            'N  2  6583.45A',
            'N  2  6548.05A',
            'N  2  5679.00A',
            'N  2  121.767m',
            'N  2  205.244m',
            'N  3  57.3238m',
            'O  1  6300.30A',
            'BLND  4363.00A',
            'O  2  3726.03A',
            'O  2  3728.81A',
            'O  2  7319.99A',
            'O  2  7329.67A',
            'O  2  7330.73A',
            'BLND  7323.00A',
            'BLND  7332.00A',
            'O  3  4958.91A',
            'O  3  5006.84A',
            'O  3  88.3323m',
            'O  3  51.8004m',
            'O  4  25.8832m',
            'S  2  6716.44A',
            'S  2  6730.82A',
            'S  3  6312.06A',
            'S  3  18.7078m',
            'S  3  33.4704m',
            'S  4  10.5076m',
            'Cl 3  5517.71A',
            'Cl 3  5537.87A',
            'O  1  63.1679m',
            'O  1  145.495m',
            'C  2  7231.33A',
            'C  2  7237.17A',
            'C  3  1906.68A',
            'C  3  1908.73A',
            'BLND  1909.00A',
            'C  2  157.636m',
            'C  1  370.269m',
            'Ar 2  6.98337m',
            'Ar 3  7135.79A',
            'Ar 3  8.98898m',
            'Ar 3  21.8253m',
            'Ar 5  7.89971m',
            'Ar 5  13.0985m',
            'Ne 2  12.8101m',
            'Ne 3  15.5509m',
            'Ne 3  36.0036m',
            'Ne 5  24.2065m',
            'Ne 5  14.3228m',
            'Ne 6  7.64318m',
            'Na 3  7.31706m',
            'Na 4  9.03098m',
            'Na 6  8.61836m',
            'Ni 2  6.63416m',
            'Ni 2  10.6793m',
            'Ni 3  7.34716m',
            'He 1  5.66958m',
            'Fe 2  5.67249m',
            'Fe 2  22.8960m',
            'Fe 2  35.7670m',
            'Fe 3  33.0270m',
            'Fe 2  51.2865m',
            'Fe 3  4658.01A',
            'Fe 3  5270.40A',
            'Fe 3  22.9190m',
            'FIR   83.0000m',
            'F12   12.0000m',
            'F25   25.0000m',
            'F60   60.0000m',
            'F100  100.000m',
            'H2    28.2130m',
            'H2    17.0300m',
            'H2    12.2752m',
            'H2    9.66228m',
            'H2    8.02362m', 
            'H2    6.90725m',
            'H2    6.10718m',
            'H2    5.50996m',
            'H2    5.05148m',
            'H2    2.12125m',
            'H2    2.22269m',
            'H2    2.03320m',
            'H2    2.24711m',
            'H2    2.20080m',
            'CO    2600.05m',
            'CO    1300.05m',
            'CO    866.727m',
            'CO    650.074m',
            'CO    520.089m',
            'CO    433.438m',
            'CO    371.549m',
            'CO    325.137m',
            'CO    289.041m',
            'CO    260.169m',
            'CO    236.549m',
            'CO    216.868m',
            'CO    200.218m',
            'CO    185.949m',
            'CO    173.584m',
            'CO    162.767m',
            'CO    153.225m',
            'CO    144.745m',
            'CO    137.159m',
            'CO    130.333m',
            'CO    124.160m',
            'CO    118.548m',
            'CO    113.427m',
            'CO    108.733m',
            'CO    104.416m',
            'CO    100.433m']
            
    options = ('Cosmic rays background','Database H2 gbar off limit -10','stop temperature linear 40K','print line faint -6', 'print last','iterate to converge','Save lines, intensity, column, emergent, all ".lines"','print line flux earth','print line precision 6','grains ISM graphite 1', 'element scale factor silicon 0.01', 'element scale factor calcium 0.01', 'element scale factor aluminium 0.01', 'element scale factor magnesium 0.01', 'element scale factor iron 0.01')         

    # Defining the object that will manage the input file for Cloudy
    c_input = pc.CloudyInput(f'{dir_}{full_model_name}')
    # Filling the object with the parameters
    # Defining the ionizing SED: Effective temperature and luminosity.
    # The lumi_unit is one of the Cloudy options, like "luminosity solar", "q(H)", "ionization parameter", etc... 
    c_input.set_BB(Teff = T, lumi_unit = 'luminosity (total)', lumi_value = L)
    # Defining the density. You may also use set_dlaw(parameters) if you have a density law defined in dense_fabden.cpp.
    c_input.set_cste_density(dens)
    # Defining the inner radius. A second parameter would be the outer radius (matter-bounded nebula).
    inner_radius = np.log10(1.0e15)
    c_input.set_radius(inner_radius)
    c_input.set_abund(predef = "GASS", nograins = True)
    c_input.set_other(options)
    c_input.set_iterate() # (0) for no iteration, () for one iteration, (N) for N iterations.
    c_input.set_sphere(True) # () or (True) : sphere, or (False): open geometry.
    c_input.set_emis_tab(emis_tab)
    dist = 1.0
    c_input.set_distance(dist, 'kpc')
    c_input.print_input(to_file = True, verbose = False)


#===============================================================

#home_dir = os.environ['HOME'] + '/'

# Changing the location and version of the cloudy executable.
pc.config.cloudy_exe = '/home/vanessa/Cloudy/c17.03/source/cloudy.exe'


# setting verbosity to medium level, change to 3 for high verbosity
pc.log_.level = 2


#===============================================================
# Parameters to be changed
#===============================================================

# Generic name of the models
model_name = f"modelo_{i}_Teff_{T_eff}_L_{luminosidade}_M_{massa_inicial}"


# The directory in which we will have the model
# You may want to change this to a different place so that the current directory
# will not receive all the Cloudy files.
dir_ = '/home/vanessa/Documentos/UNIFEI/5. TCC' + model_name + '/'

#writing the makefile in the directory dir_
pc.print_make_file(dir_ = dir_)


#ler o arquivo com o grid
grid_data = np.loadtxt('grid32.txt', skiprows=1)

# T* (K)
tab_T = grid_data[:,2]

# L* (Lsun)
ll = grid_data[:,3]
tab_L = [np.log10(a*3.826e33) for a in ll]

# log nH
tab_dens = [2., 3., 4.] 

massa_inicial = grid_data[:,0]



# Mudando razao poeira-gas, diminuindo um fator 10 
#options = ('Cosmic rays background','Database H2 gbar off limit -10','stop temperature linear 30K','print line faint -8', 'print last','iterate to converge','Save lines, intensity, column, emergent, ".lines"','print line flux earth','print line precision 6','grains ISM graphite 0.1', 'element scale factor silicon 0.01', 'element scale factor calcium 0.01', 'element scale factor aluminium 0.01', 'element scale factor magnesium 0.01', 'element scale factor iron 0.01') 


# Rodar mais tarde outras abundâncias
#       [Done] element scale factor helium 1.5
#       [Done] element scale factor carbon 5.0
#       [Done] element scale factor carbon 0.2
#       [Done] element scale factor oxygen 5.0
#       [Done] element scale factor oxygen 0.2
#       [Done] element scale factor nitrogen 5.0
#       [Done] element scale factor nitrogen 0.2
#       [Done] element scale factor sulphur 5.0
#       [Done] element scale factor sulphur 0.2
#       [Done*] element scale factor neon 5.0
#       [Done*] element scale factor neon 0.2
#       [Done] element scale factor argon 5.0
#       [Done] element scale factor argon 0.2



#===============================================================
# defining the models and writing the input files
#===============================================================

grid_size = len(tab_dens)*len(tab_T)*len(tab_L)

print(f"A total of {grid_size} models will be created.")


for L in tab_L:
  for dens in tab_dens:
    for T in tab_T:
      print L, dens, T
      make_model(dir_, model_name, T, L, dens)

#===============================================================
# Running the models using the makefile and n_proc processors
#===============================================================
# This will run cloudy models on n_proc processors. Take care!
# If you run 20 models together you will need 10 Go RAM.
n_proc = 3
pc.run_cloudy(dir_ = dir_, n_proc = n_proc, model_name = model_name, use_make = True)


#===============================================================
# All finished!    
#===============================================================
print (' ')
print ('ALL DONE!')
print ('=========================================================')
print (' ')
#===============================================================


