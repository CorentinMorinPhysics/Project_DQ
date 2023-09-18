#%%
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import scipy.io
#%%
path_to_folder = r'E:\PC Config\Documents\Fac\Cours\Semestre 9 M2\Projets\Data\Dev_WSe2_15_09_B\Good_measurements\IVDev_WSe2_15_09_B_plus_VGS_Sweep_VDS_0d2V_18_9_2023-16-14-48.mat'
mat = scipy.io.loadmat(path_to_folder)
print(mat.keys())

VDS_p = mat['VDS Bias Volt'][0]
IDS_p = mat['IDS current'][0]
VGS_p = mat['VGS'][0]
err_IDS_p = mat['IDS_error'][0]

path_to_folder = r'E:\PC Config\Documents\Fac\Cours\Semestre 9 M2\Projets\Data\Dev_WSe2_15_09_B\Good_measurements\IVDev_WSe2_15_09_B_minus_VGS_Sweep_VDS_0d2V_18_9_2023-16-16-17.mat'
mat = scipy.io.loadmat(path_to_folder)
print(mat.keys())


VDS_m = mat['VDS Bias Volt'][0]
IDS_m = mat['IDS current'][0]
VGS_m = mat['VGS'][0]
err_IDS_m = mat['IDS_error'][0]

plt.figure()
plt.errorbar(VGS_m,IDS_m,err_IDS_m)
plt.errorbar(VGS_p,IDS_p,err_IDS_p)
plt.title('VDS = 0.2V')
plt.xlabel('VGS (in V)')
plt.ylabel('IDS (in A)')

plt.figure()
plt.plot(-VGS_m,np.log(IDS_m))
plt.plot(-VGS_p,np.log(IDS_p))
plt.xlabel('VGS (in V)')
plt.ylabel('IDS (in A)')
plt.show()

# %%
