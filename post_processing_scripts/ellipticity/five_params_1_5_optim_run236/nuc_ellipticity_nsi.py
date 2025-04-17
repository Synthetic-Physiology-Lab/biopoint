import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull, convex_hull_plot_2d
from mpl_toolkits.mplot3d import Axes3D
from ellipsoid_fit import ellipsoid_fit, ellipsoid_plot, data_regularize
import matplotlib.animation as animation
string1='Atoms'
nuc_flag=0
timestep_count=0
no_nuc_part=100
file1=open("cell.xyz","r")
index = 0
nucarray=np.empty((0,4), float)
#nuc_ts_array=np.empty((0,3), float)
flat_time_array=np.empty((0,2), float)
nsi_time_array=np.empty((0,2), float)
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
    nuc_ts_array = nucarray[low_ind:upper_ind,1:4]
    #print(nuc_ts_array)
    #Plot ellipsoid on the nuclear particles based on the code described in --
    #https://github.com/aleksandrbazhin/ellipsoid_fit_python
    center, evecs, radii, v = ellipsoid_fit(nuc_ts_array)
    radii.sort()
    minor_radius = (radii[0] + radii[1])/2
    flat_coeff = (radii[2] - minor_radius) / radii[2]
    flat_row = [(i/2), flat_coeff]
    flat_time_array=np.vstack([flat_time_array,flat_row])
    data = nuc_ts_array[:,0:2]
    xx = nuc_ts_array[:,1]
    yy = nuc_ts_array[:,2]
    hull = ConvexHull(data)
    perim = hull.area
    area = hull.volume
    nsi = 4*np.pi*area/(perim**2)
    nsi_row = [i, nsi]
    nsi_time_array=np.vstack([nsi_time_array,nsi_row])
print(flat_time_array)
new_time_array=10*flat_time_array[:,0]
ellipticity=flat_time_array[:,1]
nsi_all=nsi_time_array[:,1]

fig, ax1 = plt.subplots()
plot1=ax1.plot(new_time_array[9:len_data],ellipticity[9:len_data],color='black',linestyle='--', linewidth=3)
plt.plot(new_time_array[9], ellipticity[9],'r^',markersize=16)
plt.plot(new_time_array[23], ellipticity[23],'r*',markersize=16)
ax1.plot([new_time_array[23], new_time_array[23]],[ellipticity[0], ellipticity[23]],'k:')
plt.plot(new_time_array[80], ellipticity[80],'rs',markersize=16)
ax1.plot([new_time_array[80], new_time_array[80]],[ellipticity[0], ellipticity[80]],'k:')
#plt.legend(prop={'size': 16})
ax1.set_xlabel('Time (s)', size=16)
ax1.set_ylabel('Ellipticity (-)', size=16)
ax1.tick_params(axis='x', labelsize=16)
ax1.tick_params(axis='y', labelsize=16)
#plt.xlim(20,800)

ax2=ax1.twinx()
plot2=ax2.plot(new_time_array[9:len_data],nsi_all[9:len_data],color='blue',linestyle=':', linewidth=3)
ax2.set_ylabel('NSI (-)', size=16,color='blue')
#ax2.tick_params(axis='x', labelsize=16)
ax2.tick_params(axis='y', labelsize=16,labelcolor='blue')
#ax2.set_ylim(0.7,0.9)
plt.savefig('ellip_nsi_plot.pdf',format='pdf',bbox_inches='tight')
plt.show()
