import numpy as np
import matplotlib.pyplot as plt
import pyvisa as visa
import time
from datetime import datetime
from scipy.io import savemat

#https://download.tek.com/manual/2450-900-01E_Aug_2019_User.pdf
#https://download.tek.com/manual/2450-901-01E_Sept_2019_Ref.pdf#page=179&zoom=100,69,769
#https://docs.rs-online.com/9594/0900766b81656f64.pdf

def go_to_volt_power(target,device):
    act_V = float(device.query('CH1: VOLTage?'))
    temp_V = np.arange(act_V,target,0.1)
    device.write("CH1: VOLTage 0")
    device.write('OUTPut CH1,OFF')    
    for k in range (temp):
        temp_qurey_vg = "CH1: VOLTage " + str(temp_V[i])
        device.write(temp_qurey_vg)
    temp = device.query('CH1: VOLTage?')
    print(f'Target {temp}V reached')

def my_sweep(beg,end,number_of_points,sleep_time,average_point,device):
    new_wanted_VDS = np.linspace(beg,end,number_of_points)
    IDS_meas = 0*new_wanted_VDS
    VDS_meas = 0*new_wanted_VDS
    device.write('SOUR:VOLT '+str(new_wanted_VDS[0]))
    device.write('*WAI')
    device.write("OUTP ON")
    for i in range(len(new_wanted_VDS)):
        device.write('SOUR:VOLT '+str(new_wanted_VDS[i]))
        time.sleep(0.1)
        time.sleep(sleep_time)
        for j in range(average_point):
            IDS_meas[i]+=float(device.query('MEAS:CURR?'))
            VDS_meas[i]+=float(device.query('MEAS:VOLT?'))
        IDS_meas[i]/=average_point
        VDS_meas[i]/=average_point
    device.write("OUTP OFF")
    return IDS_meas,VDS_meas

#%% Opening the ressources
rm = visa.ResourceManager()
print(rm.list_resources())
#%%
device_name = 'Dev_WSe2_12_09_A' #Enter here your device name
Description = 'IV measurements of the Device...'
save_path = 'E:\\PC Config\\Documents\\Fac\\Cours\\Semestre 9 M2\\Projets\\Data\\' # my path with / at the end
currentDateAndTime = datetime.now()
timestamp = str(currentDateAndTime.day) +'_' + str(currentDateAndTime.month)+'_' + str(currentDateAndTime.year)+"-"+str(currentDateAndTime.hour)+'-'+str(currentDateAndTime.minute)+'-'+ str(currentDateAndTime.second)
file_path= save_path + 'IV' + device_name +'_'+ timestamp +'.mat'
print(file_path)

#%%
sourcemeter_address = 'GPIB0::22::INSTR'
#powersupply_address = #Put here the Visa address of the high voltage generator
identification_request = '*IDN?'
powersupply_address = 'GPIB1::1::INSTR'
sourcemeter = rm.open_resource(sourcemeter_address)
print(f'{sourcemeter_address} : {sourcemeter.query(identification_request)}')


sourcemeter.timeout = 10*60*1e3

#%%

min_VDS = 0
max_VDS = 5
#step_VDS = 0.01
number_of_points_VDS=10
wanted_VDS = np.linspace(min_VDS,max_VDS,number_of_points_VDS)
wait_time_VDS = 0.5 #in seconds
VGS = '2V'
range_VD = np.max(np.abs(wanted_VDS))
max_IDS = 1


#%% preparing everything
str_sweep_sourcemeter = ':SOUR:SWE:VOLT:LIN '+str(min_VDS)+', '+str(max_VDS)+', '+str(number_of_points_VDS)+', '+str(wait_time_VDS)+', 1, AUTO, OFF, OFF, '+'\"bufIV\"'
query_res_sweep_sour = 'TRAC:DATA? 1, ' + str(number_of_points_VDS) +', \"bufIV\", SOUR'
query_res_sweep_amp = 'TRAC:DATA? 1, ' + str(number_of_points_VDS) +', \"bufIV\", READ'
buffer_creation = 'TRAC:MAKE \"bufIV\", ' + str(number_of_points_VDS+1)
sourcemeter.write('*RST')
sourcemeter.write('SENS:FUNC "CURR"')
sourcemeter.write('SENS:CURR:RANG:AUTO ON')
sourcemeter.write('SOUR:FUNC VOLT')
sourcemeter.write('TRAC:FILL:MODE CONT')
sourcemeter.write('SOUR:VOLT:RANG '+str(range_VD))
sourcemeter.write('SOUR:VOLT:ILIM '+str(max_IDS))

temp_ids,temp_vds = my_sweep(min_VDS,max_VDS,number_of_points_VDS,wait_time_VDS,4,sourcemeter)


mdic = {'IDS current' : temp_ids, "VGS Gate Volt": VGS,"VDS Bias Volt": temp_vds, "Wanted VDS":wanted_VDS}
savemat(file_path, mdic) 

#%%
plt.figure()
plt.plot(temp_vds,temp_ids,label='VGS=Open')
plt.xlabel('VDS (in V)')
plt.ylabel('IDS (in A)')
plt.legend()
plt.show()

sourcemeter.close()
