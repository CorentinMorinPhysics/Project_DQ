#%%
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import scipy.io
#%%
path_to_folder = 'E:\\PC Config\\Documents\\Fac\\Cours\\Semestre 9 M2\\Projets\\Data\\Dev_WSe2_15_09_B\\21_09\\IVDev_WSe2_15_09_B_both_sweep_21_9_2023-15-59-35.mat'
mat = scipy.io.loadmat(path_to_folder)
print(mat.keys())

VDS = mat['VDS Bias Volt']
IDS = mat['IDS current']
VGS = mat['VGS Gate Volt']
wanted_VDS = mat['Wanted VDS'][0,:]
print(np.argmax(VGS))
print(len(VGS[0,:]))

plt.figure()
for i in range(len(VGS[0,:])):
    plt.plot(wanted_VDS,IDS[:,i], label=f'VGS={VGS[0,i]}')
plt.xlabel('VDS (in V)')
plt.ylabel('IDS (in A)')
plt.legend()

plt.figure()
plt.plot(VGS[30,:],IDS[30,:], label=f'VDS={np.mean(wanted_VDS[i])}')
plt.legend()
plt.xlabel('VGS (in V)')
plt.ylabel('IDS (in A)')
plt.show()
# %%
