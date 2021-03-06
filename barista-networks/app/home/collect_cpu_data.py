from csv import writer
import time
from easysnmp import snmp_walk
from os import path



def get_cpu(device_list): # get current cpu utilization of all devices
        cpu_data = []
        for host_ip in device_list:
            try:
                cpu = snmp_walk('.1.3.6.1.4.1.9.9.109.1.1.1.1.6', hostname=host_ip, community='public', version=2, use_sprint_value=True)
                for item in cpu:
                    cpu_data.append(int(item.value))
            except:
                cpu_data.append(-1) # value -1 indicates SNMP connection isn't properly established
        return cpu_data


def cpu_data_main():
    filename = 'app/home/cpu.csv'
    if not path.exists(filename):
        with open(filename,'w') as f:
            header = ['R1','R2','R3','R4','R5']
            writer_f = writer(f)
            writer_f.writerow(header)
            f.close()
        
    device_list = ['198.51.100.11','198.51.100.12','198.51.100.13','198.51.100.14','198.51.100.15']
    # try:
    while True:
        with open(filename,'a') as f: # collect cpu data every 5 seconds and add to cpu.csv
            writer_f = writer(f)
            new_data = get_cpu(device_list)
            print(new_data)
            writer_f.writerow(new_data)
            f.close()
        time.sleep(5)
# except:
#     print("Configure SNMPv2c on managed devices first.")

