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

def go_to_volt_source(beg,target,device):
    if beg==target:
        device.write('SOUR:VOLT '+str(beg))
        device.write("OUTP ON")
    else:
        temp_V = np.linspace(beg,target,10)
        device.write('SOUR:VOLT '+str(temp_V[0]))
        device.write('OUTPut ON')   
        for k in range(len(temp_V)):
            device.write('SOUR:VOLT '+str(temp_V[k]))
            time.sleep(0.5)
        print(f'Target {temp_V[k]}V reached')

#%% Opening the ressources
rm = visa.ResourceManager()
print(rm.list_resources())


#%%
sourcemeter_address = 'GPIB1::18::INSTR'
powersupply_address = 'USB0::0x2A8D::0x1902::MY61001731::INSTR' #Put here the Visa address of the high voltage generator
identification_request = '*IDN?'

sourcemeter = rm.open_resource(sourcemeter_address)
print(f'{sourcemeter_address} : {sourcemeter.query(identification_request)}')
powersupply = rm.open_resource(powersupply_address)
print(f'{powersupply_address} : {powersupply.query(identification_request)}')
sourcemeter.timeout = 10*60*1e3


#%% Infos
device_name = 'Dev_WSe2_15_09_B_both_sweep' #Enter here your device name
Description = 'IV measurements of the Device...'
save_path = 'E:\\PC Config\\Documents\\Fac\\Cours\\Semestre 9 M2\\Projets\\Data\\Dev_WSe2_15_09_B\\' # my path with / at the end
currentDateAndTime = datetime.now()
timestamp = str(currentDateAndTime.day) +'_' + str(currentDateAndTime.month)+'_' + str(currentDateAndTime.year)+"-"+str(currentDateAndTime.hour)+'-'+str(currentDateAndTime.minute)+'-'+ str(currentDateAndTime.second)
file_path= save_path + 'IV' + device_name +'_'+ timestamp +'.mat'
#%% Measurment parameters

min_VDS = 0
max_VDS = 2
#step_VDS = 0.01
number_of_points_VDS=51
wait_time_VDS = 0.5 #in seconds
min_VGS = 0
max_VGS = 50
#step_VGS = 0.01
number_of_points_VGS = 5
wait_time_VGS = 0.5
max_I = 100e-9
#%% preparing everything
list_high_V = np.linspace(min_VGS,max_VGS,number_of_points_VGS)

IDS = np.zeros([number_of_points_VDS,number_of_points_VGS])
VDS = np.zeros([number_of_points_VDS,number_of_points_VGS])
VGS = np.ones([number_of_points_VDS,number_of_points_VGS])

wanted_VDS = np.linspace(min_VDS,max_VDS,number_of_points_VDS)

#%% Measuring

str_sweep_sourcemeter = ':SOUR:SWE:VOLT:LIN '+str(min_VDS)+', '+str(max_VDS)+', '+str(number_of_points_VDS)+', '+str(wait_time_VDS)+', 1, AUTO, OFF, OFF, '+'\"bufIV\"'
query_res_sweep_sour = 'TRAC:DATA? 1, ' + str(number_of_points_VDS) +', \"bufIV\", SOUR'
query_res_sweep_amp = 'TRAC:DATA? 1, ' + str(number_of_points_VDS) +', \"bufIV\", READ'
buffer_creation = 'TRAC:MAKE \"bufIV\", ' + str(number_of_points_VDS+1)
sourcemeter.write('*RST')
sourcemeter.write('SENS:FUNC "CURR"')
sourcemeter.write('SENS:CURR:RANG:AUTO ON')
sourcemeter.write('SOUR:FUNC VOLT')
sourcemeter.write('SOUR:VOLT:RANG '+str(np.max(wanted_VDS)))
sourcemeter.write('SOUR:VOLT:ILIM '+str(max_I))
sourcemeter.write(buffer_creation)
sourcemeter.write(str_sweep_sourcemeter)


powersupply.write('OUTPut OFF')

go_to_volt_power(0,list_high_V[0],powersupply)

for i in range(len(list_high_V)):
    powersupply.write('VOLTage '+str(list_high_V[i]))
    VGS[:,i]*=list_high_V[i]
    sourcemeter.write('*RST')
    sourcemeter.write('SENS:FUNC "CURR"')
    sourcemeter.write('SENS:CURR:RANG:AUTO ON')
    sourcemeter.write('SOUR:FUNC VOLT')
    sourcemeter.write('SOUR:VOLT:RANG '+str(np.max(wanted_VDS)))
    sourcemeter.write('SOUR:VOLT:ILIM '+str(max_I))
    sourcemeter.write(buffer_creation)
    sourcemeter.write(str_sweep_sourcemeter)
    sourcemeter.write(':INIT')
    sourcemeter.write('*WAI')
    temp_vds = sourcemeter.query(query_res_sweep_sour)
    temp_vds = temp_vds.split(',')
    temp_vds = (np.array(temp_vds)).astype(float)
    temp_ids = sourcemeter.query(query_res_sweep_amp)
    temp_ids = temp_ids.split(',')
    temp_ids = (np.array(temp_ids)).astype(float)
    VDS[:,i]=temp_vds
    IDS[:,i]=temp_ids
    mdic = {'IDS current' : IDS, "VGS Gate Volt": VGS,"VDS Bias Volt": VDS, "Wanted VDS":wanted_VDS}
    savemat(file_path, mdic) 
    time.sleep(wait_time_VGS)
    #/!\ Does it go back to zero ???
print(list_high_V[-1])
go_to_volt_power(list_high_V[-1],0,powersupply)

sourcemeter.write("OUTP OFF")
powersupply.write('OUTPut OFF')


#%%
plt.figure()
for i in range(len(VGS[0,:])):
    plt.plot(wanted_VDS,IDS[:,i], label=f'VGS={VGS[0,i]}')
plt.xlabel('VDS (in V)')
plt.ylabel('IDS (in A)')
plt.legend()

plt.figure()
for i in range(len(VDS[:,0])):
    plt.plot(VGS[i,:],IDS[i,:], label=f'VDS={np.mean(wanted_VDS[i])}')
plt.legend()
plt.xlabel('VGS (in V)')
plt.ylabel('IDS (in A)')
plt.show()
#%% Recording



mdic = {'IDS current' : IDS, "VGS Gate Volt": VGS,"VDS Bias Volt": VDS, "Wanted VDS":wanted_VDS}
savemat(file_path, mdic) 

#%%

sourcemeter.close()
powersupply.close()