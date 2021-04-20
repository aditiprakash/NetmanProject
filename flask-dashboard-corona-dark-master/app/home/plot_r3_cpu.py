# get data and plot R3 cpu utilization
import pandas
import matplotlib.pyplot as plt
import numpy as np

colnames = ['R1','R2','R3','R4','R5']
data = pandas.read_csv('cpu.csv',header=1,names=colnames)
r3_data = data.R3.tolist() # get all data of router R3
x_max = len(r3_data)
time = list(range(x_max))
time = [ele * 5 for ele in time]
plt.plot(time, r3_data)
plt.title('CPU Utilization of '+'R3')
plt.xlabel('Time (second)')
plt.ylabel('CPU Utilization (%)')
plt.savefig('{}_cpu.jpg'.format('R3'))
plt.show()
