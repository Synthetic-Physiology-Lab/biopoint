import numpy as np
import sys
import matplotlib.pyplot as plt

norm_stress=0

namefile='spreading_rec19_xbin_stress_zz'
position_list1=list()
stress_list1=list()
file1=open(namefile,"r")
index = 0
for line in file1:  
    index = index+1
    if index>2:
        line_list=line.split()
        position=float(line_list[0])
        vol_stress=float(line_list[1])
        position_list1.append(position)
        stress_list1.append(vol_stress)
file1.close()
abs_max_stress=abs(max(stress_list1))
abs_min_stress=abs(min(stress_list1))
norm_stress=max(abs_max_stress,abs_min_stress,norm_stress)
print(abs_max_stress)
print(abs_min_stress)

namefile='ind_xbin_stress_zz'
position_list2=list()
stress_list2=list()
file2=open(namefile,"r")
index = 0
for line in file2:  
    index = index+1
    if index>2:
        line_list=line.split()
        position=float(line_list[0])
        vol_stress=float(line_list[1])
        position_list2.append(position)
        stress_list2.append(vol_stress)
file2.close()
abs_max_stress=abs(max(stress_list2))
abs_min_stress=abs(min(stress_list2))
norm_stress=max(abs_max_stress,abs_min_stress,norm_stress)

#namefile3='constr_ybin_stress_yy'
#position_list3=list()
#stress_list3=list()
#file3=open(namefile3,"r")
#index = 0
#for line in file3:  
#    index = index+1
#    if index>2:
#        line_list=line.split()
#        position=float(line_list[0])
#        vol_stress=float(line_list[1])
#        if vol_stress!=0:
#            position_list3.append(position)
#            stress_list3.append(vol_stress)
#file3.close()
#abs_max_stress=abs(max(stress_list3))
#abs_min_stress=abs(min(stress_list3))
#norm_stress=max(abs_max_stress,abs_min_stress,norm_stress)
#print(abs_max_stress)
#print(abs_min_stress)
#print(norm_stress)
pos_shift1=max(position_list1)/2
pos_shift2=max(position_list2)/2
#pos_shift3=max(position_list3)/2

stress_list1 = [x / norm_stress for x in stress_list1]
stress_list2 = [x / norm_stress for x in stress_list2]
#stress_list3 = [x / norm_stress for x in stress_list3]

position_list1 = [x - pos_shift1 for x in position_list1]
position_list2 = [x - pos_shift2 for x in position_list2]
#position_list3 = [x - pos_shift3 for x in position_list3]

plt.figure(0)
plt.plot(position_list1, stress_list1, label='spreading, $\sigma_{zz}$')
plt.fill_between(
    x= position_list1, 
    y1= stress_list1, 
    alpha= 0.2) 
plt.xlabel('Position ($\mu m$)', size=16)
plt.ylabel('Normalized $\sigma_{zz}$', size=16)

plt.tick_params(axis='x', labelsize=16)
plt.tick_params(axis='y', labelsize=16)
#plt.ylim(-0.5,1)
#plt.xlim(-17,17)
#plt.yticks(np.arange(0,1.1,1))
#plt.legend(prop={'size': 16},frameon=False,handlelength=1,borderpad=0)
#plt.savefig('prol_2_cells_sp_bin_1b.pdf',format='pdf', bbox_inches='tight')

plt.plot(position_list2, stress_list2, label='indentation, $\sigma_{zz}$')
plt.fill_between(
    x= position_list2, 
    y1= stress_list2, 
    alpha= 0.2)
    
#plt.plot(position_list3, stress_list3, label='constriction, $\sigma_{yy}$')
#plt.fill_between(
#    x= position_list3, 
#    y1= stress_list3, 
#    alpha= 0.2)

#plt.ylim(-0.5,1)
#plt.xlim(-17,17)
#plt.xlabel('Position ($\mu m$)', size=16)
#plt.ylabel('Norm. $\sigma_{vol}$', size=16)
#plt.yticks(np.arange(0,1.1,1))
plt.tick_params(axis='x', labelsize=16)
plt.tick_params(axis='y', labelsize=16)
plt.legend(prop={'size': 16},frameon=False,handlelength=1,borderpad=0)
#plt.axis('off')
plt.savefig('spatial_bin_ind_spreading.pdf',format='pdf', bbox_inches='tight')
plt.show() 

