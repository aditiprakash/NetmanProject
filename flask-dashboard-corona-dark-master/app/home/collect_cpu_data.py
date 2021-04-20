from csv import writer
import time
from easysnmp import snmp_walk
from os import path

if not path.exists('cpu.csv'):
    with open('cpu.csv','w') as f:
        header = ['R1','R2','R3','R4','R5']
        writer_f = writer(f)
        writer_f.writerow(header)
        f.close()

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
    
device_list = ['198.51.100.11','198.51.100.12','198.51.100.13','198.51.100.14','198.51.100.15']
# try:
with open('cpu.csv','a') as f: # collect cpu data every 5 seconds and add to cpu.csv
    writer_f = writer(f)
    while True:
        new_data = get_cpu(device_list)
        writer_f.writerow(new_data)
        time.sleep(5)
# except:
#     print("Configure SNMPv2c on managed devices first.")
