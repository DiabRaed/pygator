#%%
import pygator
import numpy as np 
import matplotlib.pyplot as plt
import sympy as sp
x=y=np.linspace(-3e-3,3e-3,400)
w0=300e-6
z=0
wavelength=1064e-9
zr=np.pi*w0**2/wavelength
hg00=pygator.module.HG_mode_num(x,y,n=0,m=0,q=z+1j*zr)
hg10=pygator.module.HG_mode_num(x,y,n=1,m=0,q=z+1j*zr)

plt.imshow(np.abs(hg10['U']),cmap='jet')
plt.colorbar()

# %%

x_sym,y_sym,q_sym=sp.symbols("x_sym y_sym q")
hg00_sym=pygator.module.HG_mode_sym(x_sym,y_sym,n=0,m=0,q=q_sym)
hg10_sym=pygator.module.HG_mode_sym(x_sym,y_sym,n=1,m=0,q=q_sym)
hg00_sym['U']
# %%
#To evaluate this symbolic function at a specific point
hg00_sym['U'].subs({q_sym:0.13j,x_sym:1e-5,y_sym:1e-5})


# or to create a full space
q_val = 0.16j
x_vals = np.linspace(-3e-3, 3e-3, 400)
y_vals = np.linspace(-3e-3, 3e-3, 400)

f = sp.lambdify([q_sym, x_sym, y_sym], hg00_sym['U'], 'numpy')
X,Y=np.meshgrid(x_vals,y_vals)

hg00_sub=f(q_val,X,Y)

plt.imshow(np.abs(hg00_sub))
# %%
