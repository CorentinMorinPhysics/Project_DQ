#%%
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import scipy.io
%matplotlib qt

def set_size(w,h, ax=None):
    """ w, h: width, height in inches """
    if not ax: ax=plt.gca()
    l = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    figw = float(w)/(r-l)
    figh = float(h)/(t-b)
    ax.figure.set_size_inches(figw, figh)




#%%
path_to_folder = 'E:\\PC Config\\Documents\\Fac\\Cours\\Semestre 9 M2\\Projets\\Data\\Dev_WSe2_15_09_B\\'

number_of_points = 51
VGS = ['open open','open conncected']
IDS = np.zeros([number_of_points,len(VGS)])
VDS = np.zeros([number_of_points,len(VGS)])
path = []
path.append('IVDev_WSe2_12_09_B_VDS_sweep_VGS_still_m20_fast_0d1s_between_points_21_9_2023-15-14-49')
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
path_to_folder = 'E:\\PC Config\\Documents\\Fac\\Cours\\Semestre 9 M2\\Projets\\Data\\Dev_WSe2_15_09_B\\21_09\\'
path_to_file = 'IVDev_WSe2_12_09_B_VDS_sweep_VGS_still_m20_fast_0d1s_between_points_21_9_2023-15-14-49.mat'
file = path_to_folder + path_to_file
mat = scipy.io.loadmat(file)
IDS = mat['IDS current'][0]
VDS = mat['VDS Bias Volt'][0]
path_to_file = 'IVDev_WSe2_12_09_B_VDS_sweep_VGS_still_m20_slow_1s_between_points_21_9_2023-15-17-48.mat'
file = path_to_folder + path_to_file
mat = scipy.io.loadmat(file)
IDS_2 = mat['IDS current'][0]
VDS_2 = mat['VDS Bias Volt'][0]
path_to_file = 'IVDev_WSe2_12_09_B_VDS_sweep_VGS_still_m20_very_slow_5s_between_points_21_9_2023-15-24-4.mat'
file = path_to_folder + path_to_file
mat = scipy.io.loadmat(file)
IDS_3 = mat['IDS current'][0]
VDS_3 = mat['VDS Bias Volt'][0]
path_to_file = 'IVDev_WSe2_12_09_B_VDS_sweep_VGS_still_m20_very_slow_5s_between_points_21_9_2023-15-24-4_second_time.mat'
file = path_to_folder + path_to_file
mat = scipy.io.loadmat(file)
IDS_4 = mat['IDS current'][0]
VDS_4 = mat['VDS Bias Volt'][0]


# creating a dictionary
font = {'size': 15}
plt.rc('font', **font)

plt.figure()
plt.plot(VDS,IDS)
plt.plot(VDS_2,IDS_2)
plt.plot(VDS,IDS)
plt.plot(VDS_3,IDS_3)
plt.plot(VDS_4,IDS_4)
plt.xlabel('VGS (in V)')
plt.ylabel('IGS (in A)')
plt.legend()
plt.title('Leakage current')
set_size(5,5)
plt.show()


# %%
