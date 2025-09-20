#%%
import pygator
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
import pandas as pd
import scipy.optimize
from uncertainties import ufloat
from uncertainties import unumpy
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import subprocess
git_repo_path = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).strip().decode('utf-8')

pzts_flir_path=(Path(git_repo_path)/"Tests"/"pzts6.csv")
data=pd.read_csv(pzts_flir_path,skiprows=1,names=['z','wx','wy','std_wx','std_wy','A','B'])
data = data.apply(pd.to_numeric, errors='coerce')

# plt.plot(data['z'][:-3],data['wx'][:-3],'o',label='wx',c='b')
# plt.plot(data['z'][:-3],data['wy'][:-3],'o',label='wy',c='g')
# plt.xlabel("Distance [m]")
# plt.ylabel("Beam Size µm")
# plt.title("Beam Scan With FLIR Camera")
# plt.show()
sol_x, sol_y = pygator.module.fit_beam_profile_ODR(data['z'][:-2], data['wx'][:-2], data['z'][:-2], data['wy'][:-2], w0guess=220e-6, z0guess=0.2,wx_std=data['std_wx'][:-2], wy_std=data['std_wy'][:-2], z_std=0.005, title='FLIR Camera',print_results=True,frac_err=0.02,weight_mode='measured')# Print the results with errors
w0_experimental_x = ufloat(sol_x[0], sol_x[2])  # waist size ± error
z_experimental_x  = ufloat(sol_x[1], sol_x[3])  # waist location ± error
w0_experimental_y = ufloat(sol_y[0], sol_y[2])  # waist size ± error
z_experimental_y  = ufloat(sol_y[1], sol_y[3])  # waist location ± error

qx,qy=pygator.module.calculate_q(w0x=sol_x[0],w0y=sol_y[0],zx=sol_x[1],zy=sol_y[1])
qx_cav,qy_cav=pygator.module.calculate_q(w0x=650e-6,w0y=647e-6,zx=0.19,zy=0.19)
print(qx,qy)
#diff = qx-qy
#k = (diff.conjugate())/(qx-qy.conjugate())
#k_mag = np.sqrt(k*(k.conjugate()))
#print(k_mag)
mismatch = abs((qx - qy) / (qx - qy.conjugate()))**2
print('Mismatch between qx and qy (%):', mismatch*100)

# %%
