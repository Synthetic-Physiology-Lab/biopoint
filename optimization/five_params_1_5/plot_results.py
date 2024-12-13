import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import math

exp_data = pd.read_csv("hobson_exp_force_time.csv")
exp_time=exp_data['time'].values
exp_force=exp_data['force'].values
exp_time=exp_time-exp_time[0]
f = interp1d(exp_time, exp_force)
rmse_list=[]
iter_id_list=[]
count=0
num_iterations=242
dumpfreq=100
timestep=0.001
time_incr = dumpfreq*timestep
for i in range(num_iterations):
    count=count+1
    name_file=f"./runs/tmp_{count}/log.lammps"
    #print(name_file)
    time_list = []
    force_list = []
    with open(name_file, "r") as logfile:
         reading_forces = False
         for line in logfile:
             if "Step Temp f_indn[1] f_indn[2] f_indn[3]" in line:
                 # initiate reading from next line on
                 reading_forces = True
                 continue
             if "Loop time of" in line:
                 reading_forces = False
             if reading_forces:
                 line_list = line.split()
                 time = 1e-3 * float(line_list[0])
                 force = 1e-6 * float(line_list[4])
                 #time_list.append(time)
                 force_list.append(force)
    time=0
    newf_list=[]
    for j in range(len(force_list)):
        if j>0 and force_list[j] !=0 and force_list[j]!=force_list[(j-1)]:
            newf_list.append(force_list[j])
            time_list.append(time)
            time=time+time_incr
    MSE = np.square(np.subtract(f(time_list),newf_list)).mean() 
    RMSE = math.sqrt(MSE)
    rmse_list.append(RMSE)
    iter_id_list.append(count)
    plt.plot(time_list, newf_list)
min_rmse=min(rmse_list)
print(rmse_list)
print(min_rmse)
plt.plot(time_list, f(time_list),'ro',label='experimental')
plt.xlabel('Time (s)')
plt.ylabel('Force (nN)')
plt.legend()
plt.savefig('force_time_all_4pmin.pdf', format='pdf', bbox_inches='tight')
plt.show()
plt.plot(iter_id_list,rmse_list,'*')
plt.xlabel('Iteration ID')
plt.ylabel('RMSE (nN)')
plt.savefig('rmse_4pmin.pdf',format='pdf', bbox_inches='tight')
plt.show()
for idx in range(num_iterations):
    if rmse_list[idx]==min_rmse:
        time_list = []
        force_list = []
        print(idx)
        name_file=f"./runs/tmp_{idx+1}/log.lammps"
        with open(name_file, "r") as logfile:
             reading_forces = False
             for line in logfile:
                 if "Step Temp f_indn[1] f_indn[2] f_indn[3]" in line:
                     # initiate reading from next line on
                     reading_forces = True
                     continue
                 if "Loop time of" in line:
                     reading_forces = False
                 if reading_forces:
                     line_list = line.split()
                     time = 1e-3 * float(line_list[0])
                     force = float(line_list[4])/1000000
                     #time_list.append(time)
                     force_list.append(force)
        time=0
        newf_list=[]
        for j in range(len(force_list)):
            if j>0 and force_list[j] !=0 and force_list[j]!=force_list[(j-1)]:
                newf_list.append(force_list[j])
                time_list.append(time)
                time=time+0.1
        plt.plot(time_list, newf_list,linewidth=4)
        plt.xlabel('Time (s)')
plt.ylabel('Force (nN)')
plt.plot(time_list, f(time_list),'ro',label='experimental')
plt.savefig('best_4pmin.pdf',format='pdf', bbox_inches='tight')
plt.show()

