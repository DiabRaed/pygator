#%%
import pygator
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
import pandas as pd
# %matplotlib inline
import scipy.optimize
# from base import *
from uncertainties import ufloat
from uncertainties import unumpy
import pandas as pd
import matplotlib.pyplot as plt

#prepare and read data
pzts_flir_path=(Path(git_repo_path)/"spinview"/"data"/"pzts3.csv")
data=pd.read_csv(pzts_flir_path,skiprows=1,names=['z','wx','wy','std_wx','std_wy'])
data = data.apply(pd.to_numeric, errors='coerce')
z=data['z'][:-2]
wx=data['wx'][:-2]
wy=data['wy'][:-2]
wx_std=data['std_wx'][:-2]
wy_std=data['std_wy'][:-2]

#fit the beam size as a function of z using Orthogonal Distance Regression
sol_x, sol_y = pygator.module.fit_beam_profile_ODR(z, wx, z, wy, w0guess=220e-6, z0guess=0.11,wx_std=wx_std, wy_std=wy_std, z_std=0.005, title='FLIR Camera',print_results=True,frac_err=0.02)# Print the results with errors
w0_experimental_x = ufloat(sol_x[0], sol_x[2])  # waist size ± error
z_experimental_x  = ufloat(sol_x[1], sol_x[3])  # waist location ± error
w0_experimental_y = ufloat(sol_y[0], sol_y[2])  # waist size ± error
z_experimental_y  = ufloat(sol_y[1], sol_y[3])  # waist location ± error

#Calculate q-parameters of the fitted beam
qx,qy=pygator.module.calculate_q(w0x=sol_x[0],w0y=sol_y[0],zx=sol_x[1],zy=sol_y[1])
print(qx,qy)

#Calculate the power mismatch between the beam in x and y (quantifying the astigmatism)
mismatch = abs((qx - qy) / (qx - qy.conjugate()))**2
print('Mismatch between qx and qy (%):', mismatch*100)
# %%

