import numpy as np
from scipy.spatial import ConvexHull, convex_hull_plot_2d
import matplotlib.pyplot as plt
import pandas as pd
string1='Atoms'
nuc_flag=0
timestep_count=0
no_nuc_part=100
file1=open("cell_rec_1_19.xyz","r")
index = 0
nucarray=np.empty((0,4), float)
cellarray=np.empty((0,4), float)
#nuc_ts_array=np.empty((0,3), float)
nsi_time_array=np.empty((0,2), float)
csi_time_array=np.empty((0,2), float)
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
         x=float(line_list[1])
         y=float(line_list[2])
         z=float(line_list[3])
         cell_row=[timestep_count,x,y,z]
         cellarray=np.vstack([cellarray,cell_row])
     
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
    upper_ind = 100*(i+1)
    nuc_ts_array = []
    nuc_ts_array = nucarray[low_ind:upper_ind,:]
    data = nuc_ts_array[:,1:3]
    xx = nuc_ts_array[:,1]
    yy = nuc_ts_array[:,2]
    hull = ConvexHull(data)
    perim = hull.area
    area = hull.volume
    nsi = 4*np.pi*area/(perim**2)
    nsi_row = [i, nsi]
    nsi_time_array=np.vstack([nsi_time_array,nsi_row])
#print(len(cellarray)) 
#df = pd.DataFrame(nsi_time_array)
#df.to_csv('nsi.csv', index = False)   
for j in range(num_ts):
    low_ind2 = 1000*j
    upper_ind2 = 1000*(j+1)
    cell_ts_array = []
    cell_ts_array = cellarray[low_ind2:upper_ind2,:]
    #print(cell_ts_array)
    data2 = cell_ts_array[:,1:3]
    xx2 = cell_ts_array[:,1]
    yy2 = cell_ts_array[:,2]
    hull2 = ConvexHull(data2)
    perim2 = hull2.area
    area2 = hull2.volume
    csi = 4*np.pi*area2/(perim2**2)
    csi_row = [j, csi]
    csi_time_array=np.vstack([csi_time_array,csi_row])

#print(csi_time_array)
#print(nsi_time_array)
csi_nsi_data = np.hstack([csi_time_array,nsi_time_array])
print(csi_nsi_data)
df = pd.DataFrame(csi_nsi_data)
df.to_csv('nsi_csi_rect_1_19_n.csv', index = False)

new_time_array=10*nsi_time_array[:,0]
nsi_all=nsi_time_array[:,1]
csi_all=csi_time_array[:,1]
plt.scatter(new_time_array, nsi_all)
plt.scatter(new_time_array, csi_all)
plt.show()
