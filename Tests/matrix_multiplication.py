#%%
import pygator
import numpy as np
# Define several ABCD matrices directly
M1 = np.array([[1, 2],  # free space of 2 m
               [0, 1]])

M2 = np.array([[1, 0],  # thin lens, f=1 m
               [-1, 1]])

M3 = np.array([[0, 1],  # arbitrary matrix
               [-1, 0]])

# Multiply matrices (optical convention, reverse order)
M_total = pygator.ABCD.multimatrix.multiply_abcd(M1, M2, M3)
print("Combined ABCD matrix:\n", M_total)

# Now with q parameter
q_in = 1j * 0.5  # beam waist of 0.5 m at z=0
M_total, q_out = pygator.ABCD.multimatrix.multiply_abcd(M1, M2, M3, q_in=q_in)
print("Combined ABCD matrix:\n", M_total)
print("Output q parameter:", q_out)

# %%
