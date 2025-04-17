import numpy as np
from scipy.spatial import ConvexHull, convex_hull_plot_2d
import matplotlib.pyplot as plt
import pandas as pd

string1='Atoms'
nuc_flag=0
timestep_count=0
no_nuc_part=100
file1=open("cell.xyz","r")
index = 0
nucarray=np.empty((0,4), float)
nsi_array=np.empty((0,2), float)
# Loop through the file line by line
for line in file1:  
    index = index+1 
     
    # checking string is present in line or not
    if string1 in line:
        timestep_count+=1;
        
    line_list=line.split()
    num_list_items_0 = len(line_list)-1
    if num_list_items_0>5:
         a=line_list[num_list_items_0]
         nuc_flag=int(a)
     
    if nuc_flag == 2 and num_list_items_0>5:
         xcord=float(line_list[1])
         ycord=float(line_list[2])
         zcord=float(line_list[3])
         nuc_row=[timestep_count,xcord,ycord,zcord]
         nucarray=np.vstack([nucarray,nuc_row])
file1.close()
len_data=len(nucarray)
num_ts = int(nucarray[(len_data-1),0])
print(len_data)
print(num_ts)
for i in range(num_ts):
    low_ind = 100*i
    upper_ind = 100*(i+1)-1
    nuc_ts_array = []
    nuc_ts_array = nucarray[low_ind:upper_ind,1:3]
    hull = ConvexHull(nuc_ts_array)
    perim = hull.area
    area = hull.volume
    nsi = 4*np.pi*area/(perim**2)
    nsi_row = [i, nsi]
    nsi_array=np.vstack([nsi_array,nsi_row])
#print(nsi_array)
new_time_array=5*nsi_array[:,0]
nsi_all=nsi_array[:,1]
#print(nsi_all[4])
#print(nsi_all[23])
#print(nsi_all[80])
sim_nsi = [nsi_all[4], nsi_all[23], nsi_all[80]]
plt.figure(0)
plt.plot(new_time_array,nsi_all, linewidth=3)
plt.plot(new_time_array[9], nsi_all[9],'r^',markersize=16)
plt.plot(new_time_array[23], nsi_all[23],'r*',markersize=16)
plt.plot(new_time_array[80], nsi_all[80],'rs',markersize=16)
#plt.legend(prop={'size': 16})
plt.xlabel('Time (s)', size=16)
plt.ylabel('NSI (-)', size=16)
plt.tick_params(axis='x', labelsize=16)
plt.tick_params(axis='y', labelsize=16)
#plt.xlim(20,800)
#plt.savefig('ellip_plot.pdf',format='pdf',bbox_inches='tight')
plt.show()

df1 = pd.read_csv('exp_shape_1.csv')
data1=df1.to_numpy()
x1 = df1.iloc[:,0]
y1 = df1.iloc[:,1]
hull = ConvexHull(data1)
perim = hull.area
area = hull.volume
#print(perim,area)
nsi1 = 4*np.pi*area/(perim**2)
print(nsi1)
plt.scatter(x1,y1)
plt.plot(data1[hull.vertices,0], data1[hull.vertices,1], 'r--', lw=2)
for simplex in hull.simplices:
    plt.plot(data1[simplex, 0], data1[simplex, 1], 'k-')

df2 = pd.read_csv('exp_shape_2.csv')
x2 = df2.iloc[:,0]
y2 = df2.iloc[:,1]
data2=df2.to_numpy()
hull = ConvexHull(data2)
perim = hull.area
area = hull.volume
#print(perim,area)
nsi2 = 4*np.pi*area/(perim**2)
print(nsi2)
plt.scatter(x2,y2)
plt.plot(data2[hull.vertices,0], data2[hull.vertices,1], 'r--', lw=2)
for simplex in hull.simplices:
    plt.plot(data2[simplex, 0], data2[simplex, 1], 'k-')

df3 = pd.read_csv('exp_shape_3.csv')
x3 = df3.iloc[:,0]
y3 = df3.iloc[:,1]
data3=df3.to_numpy()
hull = ConvexHull(data3)
perim = hull.area
area = hull.volume
#print(perim,area)
nsi3 = 4*np.pi*area/(perim**2)
print(nsi3)
exp_nsi = [nsi1, nsi2, nsi3]
plt.scatter(x3,y3)
plt.plot(data3[hull.vertices,0], data3[hull.vertices,1], 'r--', lw=2)
for simplex in hull.simplices:
    plt.plot(data3[simplex, 0], data3[simplex, 1], 'k-')
plt.show()

x_sim = [0, 4, 8]
x_exp = [1, 5, 9]
plt.bar(x_sim, sim_nsi, color ='red', width = 0.8, label='sim')
plt.bar(x_exp, exp_nsi, color ='blue', width = 0.8, label='exp')
plt.xlabel('', size=16)
plt.ylabel('NSI', size=16)
plt.ylim(0,1.2)
plt.legend(prop={'size': 16},frameon=False,loc='upper center')
plt.yticks(fontsize=16)
plt.xticks([],[])
plt.yticks(np.arange(0.5, 1.1, 0.5))
plt.savefig('nsi_constriction.pdf',format='pdf', bbox_inches='tight')
plt.show()
