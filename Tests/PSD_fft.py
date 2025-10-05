#%%
import pygator
import numpy as np
import matplotlib.pyplot as plt

#Define the parameters of the signal
sampling_rate=1000 #samples/s
t0=0 #s
t1=10 #s
N=t1*sampling_rate #number of samples
t=np.linspace(t0,t1,N)
f=3 #Hz
phi=90
signal=np.sin(2*np.pi*f*t+phi)+np.sin(2*np.pi*2*f*t)
# %%
plt.plot(t,signal,label='signal')
plt.xlabel("Time [s]")
plt.ylabel("Amplitude [V]")
plt.title("A sinusoidal signal in time")
plt.legend()
plt.grid(True)
plt.show()
# %%
ff,psd,psd_db=pygator.spectran.fft_analysis.fft_psd(signal,sampling_rate)
plt.loglog(ff,psd)
# %%

#or use the Welch method to calculate the fft
ff,psd=pygator.spectran.welch_analysis.welch_psd(signal,sampling_rate)
# %%
