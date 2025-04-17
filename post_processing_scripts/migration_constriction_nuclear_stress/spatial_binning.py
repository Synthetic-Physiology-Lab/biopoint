import numpy as np
import sys
import matplotlib.pyplot as plt

norm_stress=0

namefile='soft_sp_bin_nuc_stress'
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
        if vol_stress !=0:
            if position_list1 == []:
                position_list1.append(position)
            else:
                shifted_pos=position-position_list1[0]
                position_list1.append(shifted_pos)
            stress_list1.append(vol_stress)
file1.close()
position_list1[0] = 0
abs_max_stress=abs(max(stress_list1))
abs_min_stress=abs(min(stress_list1))
norm_stress=max(abs_max_stress,abs_min_stress,norm_stress)
#for x in position_list1:
#    position_list1[x] -= position_list1[0]
print(abs_max_stress)
print(abs_min_stress)
print(position_list1)
namefile='intermediate_sp_bin_nuc_stress'
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
        if vol_stress !=0:
            if position_list2 == []:
                position_list2.append(position)
            else:
                shifted_pos=position-position_list2[0]
                position_list2.append(shifted_pos)
            stress_list2.append(vol_stress)
file2.close()
position_list2[0] = 0
abs_max_stress=abs(max(stress_list2))
abs_min_stress=abs(min(stress_list2))
norm_stress=max(abs_max_stress,abs_min_stress,norm_stress)
print(abs_max_stress)
print(abs_min_stress)

namefile='stiff_sp_bin_nuc_stress'
position_list3=list()
stress_list3=list()
file3=open(namefile,"r")
index = 0
for line in file3:  
    index = index+1
    if index>2:
        line_list=line.split()
        position=float(line_list[0])
        vol_stress=float(line_list[1])
        if vol_stress !=0:
            if position_list3 == []:
                position_list3.append(position)
            else:
                shifted_pos=position-position_list3[0]
                position_list3.append(shifted_pos)
            stress_list3.append(vol_stress)
file3.close()
position_list3[0] = 0
abs_max_stress=abs(max(stress_list3))
abs_min_stress=abs(min(stress_list3))
norm_stress=max(abs_max_stress,abs_min_stress,norm_stress)
print(abs_max_stress)
print(abs_min_stress)
print(norm_stress)

stress_list1 = [x / norm_stress for x in stress_list1]
stress_list2 = [x / norm_stress for x in stress_list2]
stress_list3 = [x / norm_stress for x in stress_list3]

pos_shift_soft=max(position_list1)/2
pos_shift_inter=max(position_list2)/2
pos_shift_stiff=max(position_list3)/2

position_list1 = [x - pos_shift_soft for x in position_list1]
position_list2 = [x - pos_shift_inter for x in position_list2]
position_list3= [x - pos_shift_stiff for x in position_list3]
print(position_list1)
#plt.figure(0)
plt.plot(position_list1, stress_list1,label='soft')
plt.fill_between(
    x= position_list1, 
    y1= stress_list1, 
    alpha= 0.2) 
plt.xlabel('Position ($\mu m$)', size=20)
plt.ylabel('Norm. $\sigma_{vol}$', size=20)

plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
#plt.ylim(-1.5,1)
#plt.xlim(-17,17)
plt.yticks(np.arange(-1,1.1,1))
#plt.legend(prop={'size': 16},frameon=False,handlelength=1,borderpad=0)
#plt.savefig('prol_2_cells_sp_bin_1b.pdf',format='pdf', bbox_inches='tight')
#plt.show()

#plt.figure(1)
plt.plot(position_list2, stress_list2,label='intermediate')
plt.fill_between(
    x= position_list2, 
    y1= stress_list2, 
    alpha= 0.2)
#plt.ylim(-1.5,1)
#plt.xlim(-17,17)
plt.xlabel('Position ($\mu m$)', size=20)
plt.ylabel('Norm. $\sigma_{vol}$', size=20)
plt.yticks(np.arange(-1,1.1,1))
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
#plt.legend(prop={'size': 16},frameon=False,handlelength=1,borderpad=0)
#plt.axis('off')
#plt.savefig('prol_2_cells_sp_bin_2b.pdf',format='pdf', bbox_inches='tight')
#plt.show() 

#plt.figure(2)
plt.plot(position_list3, stress_list3,label='stiff')
plt.fill_between(
    x= position_list3, 
    y1= stress_list3, 
    alpha= 0.2) 
#plt.ylim(-1.5,1)
#plt.xlim(-17,18)
plt.xlabel('Position ($\mu m$)', size=20)
plt.ylabel('Norm. $\sigma_{vol}$', size=20)
plt.yticks(np.arange(-1,1.1,1))
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.legend(prop={'size': 16},frameon=False,handlelength=1,borderpad=0)
#plt.axis('off')
plt.savefig('bet_2_cyl_nuc_stress.pdf',format='pdf', bbox_inches='tight')
plt.show() 
