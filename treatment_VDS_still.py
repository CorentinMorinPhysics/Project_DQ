#%%
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import scipy.io
#%%
path_to_folder = 'E:\\PC Config\\Documents\\Fac\\Cours\\Semestre 9 M2\\Projets\\Data\\Dev_WSe2_15_09_B\\Good_measurements\\'


VDS = [0.1,0.2,0.3,0.4,0.5]
IDS = np.zeros([51*2,5])
IDS_error = np.zeros([51*2,5])
VGS = np.zeros([51*2,5])
path = []
path.append('IVDev_WSe2_15_09_B_plus_VGS_Sweep_VDS_0d1V_18_9_2023-16-12-46')
path.append('IVDev_WSe2_15_09_B_minus_VGS_Sweep_VDS_0d1V_18_9_2023-16-10-49')
path.append('IVDev_WSe2_15_09_B_plus_VGS_Sweep_VDS_0d2V_18_9_2023-16-14-48')
path.append('IVDev_WSe2_15_09_B_minus_VGS_Sweep_VDS_0d2V_18_9_2023-16-16-17')
path.append( 'IVDev_WSe2_15_09_B_plus_VGS_Sweep_VDS_0d3V_18_9_2023-16-25-16')
path.append('IVDev_WSe2_15_09_B_minus_VGS_Sweep_VDS_0d3V_18_9_2023-16-22-6')
path.append('IVDev_WSe2_15_09_B_plus_VGS_Sweep_VDS_0d4V_18_9_2023-16-27-6')
path.append('IVDev_WSe2_15_09_B_minus_VGS_Sweep_VDS_0d4V_18_9_2023-16-29-1')
path.append('IVDev_WSe2_15_09_B_plus_VGS_Sweep_VDS_0d5V_18_9_2023-16-32-31')
path.append('IVDev_WSe2_15_09_B_minus_VGS_Sweep_VDS_0d5V_18_9_2023-16-30-45')

for i in range(5):
    file_minus = path_to_folder + path[2*i] + '.mat'
    mat = scipy.io.loadmat(file_minus)
    IDS[:51,i] = mat['IDS current'][0]
    IDS_error[:51,i] = mat['IDS_error'][0]
    VGS[:51,i] = mat['VGS'][0]
    file_plus = path_to_folder + path[2*i+1] + '.mat'
    mat = scipy.io.loadmat(file_plus)
    IDS[51:,i] = mat['IDS current'][0]
    VGS[51:,i] = mat['VGS'][0]
    print(VGS[51:,i])
    IDS_error[51:,i] = mat['IDS_error'][0]

plt.figure()
for i in range(5):
    plt.errorbar(VGS[:,i],IDS[:,i],IDS_error[:,i], label=f'VDS = {VDS[i]}')
plt.xlabel('VGS (in V)')
plt.ylabel('IDS (in A)')
plt.legend()
plt.show()



# %%
path_to_folder = 'E:\\PC Config\\Documents\\Fac\\Cours\\Semestre 9 M2\\Projets\\Data\\Dev_WSe2_15_09_B\\'
path_file_plus = 'IVDev_WSe2_15_09_B_plus_VGS_Sweep_VDS_0d8V_19_9_2023-11-34-26.mat'
path_file_minus = 'IVDev_WSe2_15_09_B_minus_VGS_Sweep_VDS_0d8V_19_9_2023-11-39-13.mat'

file_plus = path_to_folder + path_file_plus 
mat = scipy.io.loadmat(file_plus)
IDS_p = mat['IDS current'][0]
IDS_error_p = mat['IDS_error'][0]
VGS_p = mat['VGS'][0]
file_minus = path_to_folder + path_file_minus
mat = scipy.io.loadmat(file_minus)
IDS_m = mat['IDS current'][0]
VGS_m = mat['VGS'][0]
IDS_error_m = mat['IDS_error'][0]
print(len(IDS_p))
print(len(IDS_m))
#%%
fig, ax = plt.subplots()
ax2 = ax.twinx()
ax.errorbar(VGS_m,np.sqrt(IDS_m),IDS_error_m)
ax.errorbar(VGS_p,np.sqrt(IDS_p),IDS_error_p)
plt.ylabel('IDS (in A)')
ax2.errorbar(VGS_m,IDS_m,IDS_error_m)
ax2.errorbar(VGS_p,IDS_p,IDS_error_p)
plt.title('VDS = 0.8V')
plt.xlabel('VGS (in V)')
plt.ylabel('IDS^0.5 (in A)')
plt.show()
# %%
U = 0.8
I = 4.5e-10
print(U/I)
# %%
my_R = np.linspace(0,1e6)
my_I = 2 * my_R/(my_R + 10e3)
plt.plot(my_R,my_I)
# %%
plt.figure()
plt.plot(VGS_m,np.log10((((0.8-(1.9e9*IDS_m))/(IDS_m)))))
plt.plot(VGS_p,np.log10(((0.8-(1.9e9*IDS_p))/IDS_p)))
plt.show()

plt.figure()
plt.plot(VGS_m,(0.8-(1.9e9*IDS_m)))
plt.show()
# %%
print(np.max(0.8/IDS_p))

# %%
