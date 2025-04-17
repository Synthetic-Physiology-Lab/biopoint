import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv("results_force.csv")
mean = data['mean'].values/1000000
std = data['std'].values/1000000
p_10 = data['p_10'].values/1000000
p_90 = data['p_90'].values/1000000

mean_list=list()
std_list=list()
p_10_list=list()
p_90_list=list()
time_list=list()
sobol_first_eta0_list=list()
sobol_first_kappa0_list=list()
sobol_first_k_nuc_list=list()
sobol_first_v_nuc_list=list()
sobol_first_k12_list=list()
sobol_first_mylambda_list=list()
sobol_total_eta0_list=list()
sobol_total_kappa0_list=list()
sobol_total_k_nuc_list=list()
sobol_total_v_nuc_list=list()
sobol_total_k12_list=list()
sobol_total_mylambda_list=list()
lower_list=list()
upper_list=list()

sobol_first_eta0 = data['sobol_first_eta0'].values
sobol_first_kappa0 = data['sobol_first_kappa0'].values
sobol_first_k_nuc = data['sobol_first_kappa_nuc'].values
sobol_first_v_nuc = data['sobol_first_eta_nuc'].values
sobol_first_k12 = data['sobol_first_k12'].values
sobol_first_mylambda = data['sobol_first_mylambda'].values

sobol_total_eta0 = data['sobol_total_eta0'].values
sobol_total_kappa0 = data['sobol_total_kappa0'].values
sobol_total_k_nuc = data['sobol_total_kappa_nuc'].values
sobol_total_v_nuc = data['sobol_total_eta_nuc'].values
sobol_total_k12 = data['sobol_total_k12'].values
sobol_total_mylambda = data['sobol_total_mylambda'].values

time=0
for i in range(len(mean)):
    if i>0 and mean[i] !=0 and mean[i]!=mean[(i-1)]:
        mean_list.append(mean[i])
        std_list.append(std[i])
        lower_list.append(mean[i]-std[i])
        upper_list.append(mean[i]+std[i])
        p_10_list.append(p_10[i])
        p_90_list.append(p_90[i])
        sobol_first_eta0_list.append(sobol_first_eta0[i])
        sobol_first_kappa0_list.append(sobol_first_kappa0[i])
        sobol_first_k_nuc_list.append(sobol_first_k_nuc[i])
        sobol_first_v_nuc_list.append(sobol_first_v_nuc[i])
        sobol_first_k12_list.append(sobol_first_k12[i])
        sobol_first_mylambda_list.append(sobol_first_mylambda[i])
        sobol_total_eta0_list.append(sobol_total_eta0[i])
        sobol_total_kappa0_list.append(sobol_total_kappa0[i])
        sobol_total_k_nuc_list.append(sobol_total_k_nuc[i])
        sobol_total_v_nuc_list.append(sobol_total_v_nuc[i])
        sobol_total_k12_list.append(sobol_total_k12[i])
        sobol_total_mylambda_list.append(sobol_total_mylambda[i])
        time_list.append(time)
        time=time+0.1

exp_data = pd.read_csv("hobson_exp_force_time.csv")
exp_time=exp_data['time'].values
exp_force=exp_data['force'].values

exp_time=exp_time-exp_time[0]

plt.plot(time_list, mean_list,label='mean, standard deviation')
plt.xlabel('Time (s)',size=16)
plt.ylabel('Force (nN)',size=16)
plt.fill_between(time_list, lower_list, upper_list, alpha=0.5)
#plt.plot(exp_time, exp_force,'r', label='experimental')
plt.legend(prop={'size': 16})
plt.tick_params(axis='x', labelsize=16)
plt.tick_params(axis='y', labelsize=16)
plt.savefig('mean_std.pdf',format='pdf', bbox_inches='tight')
plt.show()

plt.plot(time_list, mean_list,label='mean, 10-90% CI')
plt.xlabel('Time (s)',size=16)
plt.ylabel('Force (nN)',size=16)
plt.fill_between(time_list, p_10_list, p_90_list, alpha=0.5)
#plt.plot(exp_time, exp_force,'r',label='experimental')
plt.legend(prop={'size': 16})
plt.tick_params(axis='x', labelsize=16)
plt.tick_params(axis='y', labelsize=16)
plt.savefig('conf_interval_10_90.pdf',format='pdf', bbox_inches='tight')
plt.show()

plt.plot(time_list,sobol_first_kappa0_list, label='stiffness')
plt.plot(time_list,sobol_first_eta0_list, label='viscosity')
plt.plot(time_list,sobol_first_k_nuc_list, label='nuclear_stiffness')
plt.plot(time_list,sobol_first_v_nuc_list, label='nuclear viscosity')
plt.plot(time_list,sobol_first_k12_list, label='k12')
plt.plot(time_list,sobol_first_mylambda_list, label='tuning coeff.')
plt.title('Influence of individual parameters')
plt.legend()
plt.savefig('parameter_effect.pdf',format='pdf', bbox_inches='tight')
plt.show()

plt.plot(time_list,sobol_total_kappa0_list, label='stiffness')
plt.plot(time_list,sobol_total_eta0_list, label='viscosity')
plt.plot(time_list,sobol_total_k_nuc_list, label='k_scaling_nuclear_stiffness')
plt.plot(time_list,sobol_total_v_nuc_list, label='v_scaling_nuc')
plt.plot(time_list,sobol_total_k12_list, label='k12')
plt.plot(time_list,sobol_total_mylambda_list, label='tuning coeff.')
plt.legend()
#plt.savefig('parameter_effect_total.jpg')
plt.show()
