#%%
import pygator

#test from JamMt #300 mm lens at 34cm with input beam at 0 of waist 370 µm
fx,fy=pygator.module.calculate_focal_length(w0x_in=370e-6,w0y_in=370e-6,zx_in=40e-2,zy_in=34e-2,
w0x_out=273e-6,w0y_out=273e-6,zx_out=-32e-2,zy_out=-32e-2)
print(fx,fy)


# %%
