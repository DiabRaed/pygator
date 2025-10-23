#%%
import pygator 
import numpy as np
import matplotlib.pyplot as plt 
import sympy as sp 
import subprocess
from pathlib import Path
git_repo_path = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).strip().decode('utf-8')
base_path = Path(git_repo_path) / "random_scripts" 
from scipy.signal import welch

# The goal is to reconstruct the phase of this beam using Novak PSA
# https://www.sciencedirect.com/science/article/pii/S0030402604702260
x=y=np.linspace(-3e-3,3e-3,400)
w0=700e-6
z=1e-2
wavelength=1064e-9
zr=np.pi*w0**2/wavelength
hg00=pygator.module.HG_mode_num(x,y,n=0,m=0,q=z+1j*zr)
hg10=pygator.module.HG_mode_num(x,y,n=1,m=0,q=z+1j*zr)


extend=[x.min()/1e-3,x.max()/1e-3,y.min()/1e-3,y.max()/1e-3]
signal=hg00['U']#+0.1*hg10['U']
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# Magnitude plot
im0 = axs[0].imshow(np.abs(signal),extent=extend, cmap='jet')
axs[0].set_title('Magnitude')
axs[0].set_xlabel("x-coordinates [mm]")
axs[0].set_xlabel("y-coordinates [mm]")
plt.colorbar(im0, ax=axs[0])

# Phase plot.. let's try to reconstruct this from Novak algorithm
im1 = axs[1].imshow(np.angle(signal),extent=extend, cmap='jet')
axs[1].set_title('Phase')
axs[1].set_xlabel("x-coordinates [mm]")
axs[1].set_xlabel("y-coordinates [mm]")
plt.colorbar(im1, ax=axs[1])
plt.suptitle("Magnitude and phase of the beam to recover")
plt.tight_layout()
plt.savefig((Path(git_repo_path) / "random_scripts"/"plots"/"beam.pdf"))

plt.show()

#%%
# Let's create 5 intensity images at 0, pi/2,pi,3pi/2,2pi

phi = np.angle(signal)              # true phase 
B = np.abs(signal)**2/np.max(np.abs(signal)**2)  # normalized intensity
A = 0*np.mean(B)                    # constant phase shift.. make it zero

deltas = [0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
I = [A + B * np.cos(phi + d) for d in deltas]


save_path = Path(git_repo_path) / "random_scripts" / "plots"

plt.figure(figsize=(12, 8))

for idx, img in enumerate(I):
    plt.subplot(2, 3, idx+1)
    plt.imshow(img, cmap='jet', extent=extend, origin='lower')
    plt.title(f"δ = {deltas[idx]/np.pi:.1f} π")
    plt.xlabel("x [mm]")
    plt.ylabel("y [mm]")
    plt.colorbar(fraction=0.046, pad=0.04)

# Optional: leave the 6th subplot empty
plt.subplot(2,3,6)
plt.axis('off')

plt.tight_layout()
plt.savefig(save_path / "intensity_cycle_grid.pdf")
plt.show()
# %%

def novak(lis):
    den = 2*lis[2]-lis[0]-lis[4]
    A = lis[1]-lis[3]
    B = lis[0]-lis[4]
    num = np.sqrt(abs(4*A**2-B**2))
    pm = np.sign(A)
    return np.arctan2(pm*num,den)


recovered_PSA=novak(I)
plt.imshow(recovered_PSA,cmap='jet')
plt.colorbar()
# %%


# unwrap recovered phase along both axes
recovered_unwrapped = np.unwrap(recovered_PSA, axis=0)
recovered_unwrapped = np.unwrap(recovered_unwrapped, axis=1)

plt.figure(figsize=(12, 5))

#original phase
plt.subplot(1, 2, 1)
plt.imshow(phi, cmap='jet', extent=extend, origin='lower')
plt.title("Original phase")
plt.xlabel("x [mm]")
plt.ylabel("y [mm]")
plt.colorbar(fraction=0.046, pad=0.04)

#recovered Novak phase
plt.subplot(1, 2, 2)
plt.imshow(recovered_unwrapped, cmap='jet', extent=extend, origin='lower')
plt.title("Recovered Novak phase")
plt.xlabel("x [mm]")
plt.ylabel("y [mm]")
plt.colorbar(fraction=0.046, pad=0.04)

plt.tight_layout()
plt.savefig(Path(git_repo_path) / "random_scripts" / "plots" / "recovered_phase.pdf")
plt.show()


# %%
print("Original phase: max - min: ",phi.max()-phi.min())
print("Recovered phase: max - min: ",recovered_unwrapped.max()-recovered_unwrapped.min())
# %%
