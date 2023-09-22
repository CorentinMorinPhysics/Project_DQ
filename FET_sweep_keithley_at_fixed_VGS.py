#%%
import numpy as np
import matplotlib.pyplot as plt
import pyvisa as visa
import time
from datetime import datetime
from scipy.io import savemat

#https://download.tek.com/manual/2450-900-01E_Aug_2019_User.pdf
#https://download.tek.com/manual/2450-901-01E_Sept_2019_Ref.pdf#page=179&zoom=100,69,769
#https://docs.rs-online.com/9594/0900766b81656f64.pdf

def go_to_volt_power(beg,target,device):
    if beg==target:
        device.write('VOLTage '+str(beg))
        device.write('OUTPut ON') 
    else:
        temp_V = np.linspace(beg,target,10)
        device.write('VOLTage '+str(temp_V[0]))
        device.write('OUTPut ON')   
        for k in range(len(temp_V)):
            device.write('VOLTage '+str(temp_V[k]))
            time.sleep(0.5)
        print(f'Target {temp_V[k]}V reached')

#%% Opening the ressources
rm = visa.ResourceManager()
print(rm.list_resources())
#%%

#%%
sourcemeter_address = 'GPIB1::18::INSTR'
powersupply_address = 'USB0::0x2A8D::0x1902::MY61001731::INSTR' #Put here the Visa address of the high voltage generator
identification_request = '*IDN?'
sourcemeter = rm.open_resource(sourcemeter_address)
print(f'{sourcemeter_address} : {sourcemeter.query(identification_request)}')
powersupply = rm.open_resource(powersupply_address)
print(f'{powersupply_address} : {powersupply.query(identification_request)}')

sourcemeter.timeout = 10*60*1e3

#%%

min_VDS = 0
max_VDS = 5
#step_VDS = 0.01
number_of_points_VDS=51
wait_time_VDS = 5 #in seconds
VGS = -20
max_I = 10e-6

IDS = np.zeros([number_of_points_VDS,1])
VDS = np.zeros([number_of_points_VDS,1])

wanted_VDS = np.linspace(min_VDS,max_VDS,number_of_points_VDS)

#%% preparing everything
str_sweep_sourcemeter = ':SOUR:SWE:VOLT:LIN '+str(min_VDS)+', '+str(max_VDS)+', '+str(number_of_points_VDS)+', '+str(wait_time_VDS)+', 1, AUTO, OFF, OFF, '+'\"bufIV\"'
query_res_sweep_sour = 'TRAC:DATA? 1, ' + str(number_of_points_VDS) +', \"bufIV\", SOUR'
query_res_sweep_amp = 'TRAC:DATA? 1, ' + str(number_of_points_VDS) +', \"bufIV\", READ'
buffer_creation = 'TRAC:MAKE \"bufIV\", ' + str(number_of_points_VDS+1)
powersupply.write('OUTPut OFF')
sourcemeter.write('*RST')
sourcemeter.write('SENS:FUNC "CURR"')
sourcemeter.write('SENS:CURR:RANG:AUTO ON')
sourcemeter.write('SOUR:FUNC VOLT')
sourcemeter.write('SOUR:VOLT:RANG '+str(np.max(wanted_VDS)))
sourcemeter.write('SOUR:VOLT:ILIM '+str(max_I))
sourcemeter.write(buffer_creation)
sourcemeter.write(str_sweep_sourcemeter)

go_to_volt_power(0,np.abs(VGS),powersupply)

sourcemeter.write('INIT')
sourcemeter.write('*WAI')

temp_vds = sourcemeter.query(query_res_sweep_sour)
temp_vds = temp_vds.split(',')
temp_vds = (np.array(temp_vds)).astype(float)
temp_ids = sourcemeter.query(query_res_sweep_amp)
temp_ids = temp_ids.split(',')
temp_ids = (np.array(temp_ids)).astype(float)

go_to_volt_power(np.abs(VGS),0,powersupply)
powersupply.write("OUTP OFF")


#%%
plt.figure()
plt.plot(temp_vds,temp_ids,label=f'VGS={VGS}')
plt.xlabel('VDS (in V)')
plt.ylabel('IDS (in A)')
plt.legend()
plt.show()
#%%
device_name = 'Dev_WSe2_12_09_B_VDS_sweep_VGS_still_m20_fast_0d1s_between_points' #Enter here your device name
Description = 'IV measurements of the Device...'
save_path = 'E:\\PC Config\\Documents\\Fac\\Cours\\Semestre 9 M2\\Projets\\Data\\\\Dev_WSe2_15_09_B\\' # my path with / at the end
currentDateAndTime = datetime.now()
timestamp = str(currentDateAndTime.day) +'_' + str(currentDateAndTime.month)+'_' + str(currentDateAndTime.year)+"-"+str(currentDateAndTime.hour)+'-'+str(currentDateAndTime.minute)+'-'+ str(currentDateAndTime.second)
file_path= save_path + 'IV' + device_name +'_'+ timestamp +'.mat'

mdic = {'IDS current' : temp_ids, "VGS Gate Volt": VGS,"VDS Bias Volt": temp_vds, "Wanted VDS":wanted_VDS}
savemat(file_path, mdic) 

#%%
sourcemeter.close()
powersupply.close()
# %%
