#%%
import pygator
import numpy as np 
import matplotlib.pyplot as plt
import sympy as sp

#Let's build numerical HG modes
x=y=np.linspace(-3e-3,3e-3,400)
w0=400e-6
z=0
wavelength=1064e-9
zr=np.pi*w0**2/wavelength
hg00=pygator.module.HG_mode_num(x,y,n=0,m=0,q=z+1j*zr)
hg10=pygator.module.HG_mode_num(x,y,n=1,m=0,q=z+1j*zr)


extend=[x.min(),x.max(),y.min(),y.max()]
signal=hg00['U']
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# Magnitude plot
im0 = axs[0].imshow(np.abs(signal),extent=extend, cmap='jet')
axs[0].set_title('Magnitude')
plt.colorbar(im0, ax=axs[0])

# Phase plot
im1 = axs[1].imshow(np.angle(signal),extent=extend, cmap='jet')
axs[1].set_title('Phase')
plt.colorbar(im1, ax=axs[1])

plt.tight_layout()
plt.show()
# %%
# Or we can build HG modes symbolically 
x_sym,y_sym,q_sym=sp.symbols("x_sym y_sym q")
hg00_sym=pygator.module.HG_mode_sym(x_sym,y_sym,n=0,m=0,q=q_sym)
hg10_sym=pygator.module.HG_mode_sym(x_sym,y_sym,n=1,m=0,q=q_sym)
hg00_sym['U']


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


# %%
#We can also compare it to FINESSE
try:
    import finesse
    from finesse.gaussian import BeamParam, HGMode

    w0 = 1e-3
    zR = np.pi*w0**2/wavelength

    q_0 = 0+1j*zR # at the waist

    R_TM = 2*w0
    num_pts = 1201
    center_idx = (num_pts - 1) // 2

    x_tm = y_tm = np.linspace(-R_TM, R_TM, num_pts)
    xx, yy = np.meshgrid(x_tm, y_tm)

    hg00=pygator.module.HG_mode_num(x_tm,y_tm,n=1,m=0,q=q_0)

    ###########################
    HG00_0 = HGMode(q_0, n=0, m=1)
    HG00_data_0 = HG00_0.unm(x_tm, y_tm)

    extend=[xx.min(),xx.max(),yy.min(),yy.max()]
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    # Magnitude plot
    im0 = axs[0].imshow(np.abs(HG00_data_0),extent=extend, cmap='jet')
    axs[0].set_title('Magnitude - FINESSE')
    plt.colorbar(im0, ax=axs[0])

    # Phase plot
    im1 = axs[1].imshow(np.angle(HG00_data_0),extent=extend, cmap='jet')
    axs[1].set_title('Phase - FINESSE')
    plt.colorbar(im1, ax=axs[1])

    plt.tight_layout()
    plt.show()


    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    # Magnitude plot
    im0 = axs[0].imshow(np.abs(hg00['U']),extent=extend,cmap='jet')
    axs[0].set_title('Magnitude - pygator')
    plt.colorbar(im0, ax=axs[0])

    # Phase plot
    im1 = axs[1].imshow(np.angle(hg00['U']),extent=extend, cmap='jet')
    axs[1].set_title('Phase - pygator')
    plt.colorbar(im1, ax=axs[1])

    plt.tight_layout()
    plt.show()
except:
    print("Can't find FINESSE")
    # %%
