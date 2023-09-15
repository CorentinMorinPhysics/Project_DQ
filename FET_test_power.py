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

#%% Opening the ressources
rm = visa.ResourceManager()
print(rm.list_resources())


#%%
sourcemeter_address = 'GPIB0::22::INSTR'
identification_request = '*IDN?'
powersupply_address = 'GPIB1::1::INSTR'

sourcemeter = rm.open_resource(sourcemeter_address)
print(f'{sourcemeter_address} : {sourcemeter.query(identification_request)}')
powersupply = rm.open_resource(powersupply_address)
print(f'{powersupply_address} : {powersupply.query(identification_request)}')

sourcemeter.timeout = 10*60*1e3

#%%

min_VDS = 0
max_VDS = 5
#step_VDS = 0.01
number_of_points_VDS=11
wait_time_VDS = 0.5 #in seconds
min_VGS = 0
max_VGS = 5
#step_VGS = 0.01
number_of_points_VGS = 100
wait_time_VGS = 0.5



powersupply.write('*RST')
powersupply.write('VOLTage 0')



sourcemeter.close()
powersupply.close()

