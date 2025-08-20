#%%
import pygator

#This script reads beam sizes from the wincam saved as a single 
# text file. 
date='Aug 15, 2025'
file_path=(Path(git_repo_path)/"Beam_scan"/f"{date}"/"test8.txt")
wx,wy,wx_std,wy_std,z,times=fs.read_beam_profile_continous(file_path=file_path,start_position=0,end_position=15,print_files=False)

#Here we provide the the aboove read beam sizes and distances to the ODR fit 
# function. It returns beam sizes as the mean of each time slice 
# plus the standard deviation of the time 
sol_x, sol_y = pygator.module.fit_beam_profile_ODR(z, wx, z, wy, w0guess=239e-6, z0guess=0.1, zRguess=0.2, wx_std=wx_std, wy_std=wy_std, z_std=0.005, title='Reflection',print_results=True,frac_err=0.02)# Print the results with errors
w0_experimental_x = ufloat(sol_x[0], sol_x[3])  # waist size ± error
z_experimental_x  = ufloat(sol_x[1], sol_x[4])  # waist location ± error
zR_experimental_x = ufloat(sol_x[2], sol_x[5])  # Rayleigh range ± error
w0_experimental_y = ufloat(sol_y[0], sol_y[3])  # waist size ± error
z_experimental_y  = ufloat(sol_y[1], sol_y[4])  # waist location ± error
zR_experimental_y = ufloat(sol_y[2], sol_y[5])  # Rayleigh range ± error

# A function to calculate the q-parameter given waist position and waist size
qx,qy=pygator.module.calculate_q(w0x=sol_x[0],w0y=sol_y[0],zx=sol_x[1],zy=sol_y[1])
qx_cav,qy_cav=pygator.module.calculate_q(w0x=650e-6,w0y=647e-6,zx=0.19,zy=0.19)

#A function to calculate the mismatch between 2 q-parameters
print(fs.mismatch_calculator(q1=qx,q2=qx_cav))
print(fs.mismatch_calculator(q1=qy,q2=qy_cav))
# %%


# %%
