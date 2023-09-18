#%%
import numpy as np
import matplotlib.pyplot as plt
import pyvisa as visa
import time
from datetime import datetime
from scipy.io import savemat

#%%
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
powersupply_address = 'GPIB1::1::INSTR' #Put here the Visa address of the high voltage generator
identification_request = '*IDN?'

sourcemeter = rm.open_resource(sourcemeter_address)
print(f'{sourcemeter_address} : {sourcemeter.query(identification_request)}')
powersupply = rm.open_resource(powersupply_address)
print(f'{powersupply_address} : {powersupply.query(identification_request)}')
sourcemeter.timeout = 10*60*1e3



VDS = 0.5
min_VGS = 0
max_VGS = 25
number_of_points_VGS = 51
wait_time_VGS = 0.5
max_I = 100e-9

number_of_points_avg = 5
#%% preparing everything
list_high_V = np.linspace(min_VGS,max_VGS,number_of_points_VGS)
my_IDS = 0*list_high_V
my_err_IDS = 0*list_high_V
temp_IDS = np.zeros([1,number_of_points_avg])
#%%
sourcemeter.write('*RST')
powersupply.write('*RST')
sourcemeter.write('SENS:FUNC "CURR"')
sourcemeter.write('SENS:CURR:RANG:AUTO ON')
sourcemeter.write('SOUR:FUNC VOLT')
sourcemeter.write('SOUR:VOLT:RANG '+str(VDS))
sourcemeter.write('SOUR:VOLT:ILIM '+str(max_I))

go_to_volt_source(0,VDS,sourcemeter)

go_to_volt_power(0,list_high_V[0],powersupply)

for i in range(len(list_high_V)):
    powersupply.write('VOLTage '+str(list_high_V[i]))
    time.sleep(wait_time_VGS)
    for j in range(number_of_points_avg):
        temp_IDS[0,j] = float(sourcemeter.query('MEAS:CURR?'))
    
    my_IDS[i] = np.mean(temp_IDS)
    my_err_IDS[i] = np.std(temp_IDS)

go_to_volt_source(VDS,0,sourcemeter)
sourcemeter.write("OUTP OFF")
go_to_volt_power(list_high_V[-1],0,powersupply)
powersupply.write("OUTP OFF")
# %%

name_file = 'VGS_Sweep_VDS_0d5V'
polarity_power = 'plus'
Description = 'IV measurements of the Device...'
save_path = 'E:\\PC Config\\Documents\\Fac\\Cours\\Semestre 9 M2\\Projets\\Data\\Dev_WSe2_15_09_B\\Good_measurements\\' # my path with / at the end
currentDateAndTime = datetime.now()
timestamp = str(currentDateAndTime.day) +'_' + str(currentDateAndTime.month)+'_' + str(currentDateAndTime.year)+"-"+str(currentDateAndTime.hour)+'-'+str(currentDateAndTime.minute)+'-'+ str(currentDateAndTime.second)


if polarity_power=='minus':
    device_name = 'Dev_WSe2_15_09_B_minus_'+name_file #Enter here your device name
    file_path= save_path + 'IV' + device_name +'_'+ timestamp +'.mat'
    print(file_path)

    mdic = {'IDS current' : my_IDS, "IDS_error": my_err_IDS,"VDS Bias Volt": VDS, "VGS":(-list_high_V)}
    savemat(file_path, mdic) 
    plt.figure()
    plt.errorbar(-list_high_V,my_IDS,my_err_IDS)
    plt.show()
elif polarity_power=='plus':
    device_name = 'Dev_WSe2_15_09_B_plus_'+name_file #Enter here your device name
    file_path= save_path + 'IV' + device_name +'_'+ timestamp +'.mat'
    print(file_path)

    mdic = {'IDS current' : my_IDS, "IDS_error": my_err_IDS,"VDS Bias Volt": VDS, "VGS":(list_high_V)}
    savemat(file_path, mdic) 
    plt.figure()
    plt.errorbar(list_high_V,my_IDS,my_err_IDS)
    plt.show()
