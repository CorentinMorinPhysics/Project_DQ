#%%
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import scipy.io
#%%
path_to_folder = 'E:\\PC Config\\Documents\\Fac\\Cours\\Semestre 9 M2\\Projets\\Data\\Dev_WSe2_15_09_B\\'

number_of_points = 51
VGS = ['open open','open conncected']
IDS = np.zeros([number_of_points,len(VGS)])
VDS = np.zeros([number_of_points,len(VGS)])
path = []
path.append('IVDev_WSe2_12_09_B_VDS_sweep_VGS_open_19_9_2023-11-6-28')
path.append('IVDev_WSe2_12_09_B_VDS_sweep_VGS_open_but_connected_to_source_19_9_2023-11-9-36')


for i in range(len(VGS)):
    file = path_to_folder + path[i] + '.mat'
    mat = scipy.io.loadmat(file)
    IDS[:,i] = mat['IDS current'][0]
    VDS[:,i] = mat['VDS Bias Volt'][0]


plt.figure()
for i in range(len(VGS)):
    plt.plot(VDS[:,i],IDS[:,i],label=f'VGS={VGS[i]}')
plt.xlabel('VDS (in V)')
plt.ylabel('IDS (in A)')
plt.legend()
plt.show()


# %%
path_to_folder = 'E:\\PC Config\\Documents\\Fac\\Cours\\Semestre 9 M2\\Projets\\Data\\Dev_WSe2_15_09_B\\'
path_to_file = 'IVDev_WSe2_12_09_B_VDS_sweep_VGS_still_test_symmetry_19_9_2023-12-4-9.mat'
file = path_to_folder + path_to_file
mat = scipy.io.loadmat(file)
IDS = mat['IDS current'][0]
VDS = mat['VDS Bias Volt'][0]
plt.figure()
plt.plot(VDS,IDS)
plt.xlabel('VGS (in V)')
plt.ylabel('IGS (in A)')
plt.legend()
plt.title('Leakage current')
plt.show()
# %%
