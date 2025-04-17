import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
final_data=np.empty((0,2), float)
circle_data = pd.read_csv("nsi_csi_circle_n.csv")
circle_time=circle_data['0'].values
circle_csi=circle_data['1'].values
circle_nsi=circle_data['3'].values
data_length=len(circle_csi)-1
circle_final=[circle_csi[data_length], circle_nsi[data_length]]
final_data = np.vstack([final_data,circle_final])

square_data = pd.read_csv("nsi_csi_square_n.csv")
square_time=square_data['0'].values
square_csi=square_data['1'].values
square_nsi=square_data['3'].values
square_final=[square_csi[data_length], square_nsi[data_length]]
final_data = np.vstack([final_data,square_final])

triangle_data = pd.read_csv("nsi_csi_triangle_n.csv")
triangle_time=triangle_data['0'].values
triangle_csi=triangle_data['1'].values
triangle_nsi=triangle_data['3'].values
triangle_final=[triangle_csi[data_length], triangle_nsi[data_length]]
final_data = np.vstack([final_data,triangle_final])

rect_1_3_data = pd.read_csv("nsi_csi_rect_1_3_n.csv")
rect_1_3_time=rect_1_3_data['0'].values
rect_1_3_csi=rect_1_3_data['1'].values
rect_1_3_nsi=rect_1_3_data['3'].values
rect_1_3_final=[rect_1_3_csi[data_length], rect_1_3_nsi[data_length]]
final_data = np.vstack([final_data,rect_1_3_final])

rect_1_7_data = pd.read_csv("nsi_csi_rect_1_7_n.csv")
rect_1_7_time=rect_1_7_data['0'].values
rect_1_7_csi=rect_1_7_data['1'].values
rect_1_7_nsi=rect_1_7_data['3'].values
rect_1_7_final=[rect_1_7_csi[data_length], rect_1_7_nsi[data_length]]
final_data = np.vstack([final_data,rect_1_7_final])

rect_1_19_data = pd.read_csv("nsi_csi_rect_1_19_n.csv")
rect_1_19_time=rect_1_19_data['0'].values
rect_1_19_csi=rect_1_19_data['1'].values
rect_1_19_nsi=rect_1_19_data['3'].values
rect_1_19_final=[rect_1_19_csi[data_length], rect_1_19_nsi[data_length]]
final_data = np.vstack([final_data,rect_1_19_final])

literature_data = pd.read_excel('nsi_csi_data.xlsx')
print(literature_data)

plt.figure(0)
plt.plot(circle_time,circle_csi,'o',linestyle='None',label='Circle')
plt.plot(square_time,square_csi,'s',linestyle='None',label='Square')
plt.plot(triangle_time,triangle_csi,'^',linestyle='None',label='Triangle')
plt.plot(rect_1_3_time,rect_1_3_csi,'*',linestyle='None',label='Rectangle 1')
plt.plot(rect_1_7_time,rect_1_7_csi,'+',linestyle='None',label='Rectangle 2')
plt.plot(rect_1_19_time,rect_1_19_csi,'x',linestyle='None',label='Rectangle 3')
#plt.legend(prop={'size': 16})
plt.xlabel('Time (s)', size=16)
plt.ylabel('Cell Shape Index', size=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xticks(np.arange(0, 110, 100))
plt.yticks(np.arange(0.2, 1.1, 0.4))
plt.savefig('csi_time.pdf',format='pdf', bbox_inches='tight')
plt.show()

plt.figure(1)
plt.plot(circle_time,circle_nsi,'o',linestyle='None',label='Circle')
plt.plot(square_time,square_nsi,'s',linestyle='None',label='Square')
plt.plot(triangle_time,triangle_nsi,'^',linestyle='None',label='Triangle')
plt.plot(rect_1_3_time,rect_1_3_nsi,'*',linestyle='None',label='Rectangle 1')
plt.plot(rect_1_7_time,rect_1_7_nsi,'+',linestyle='None',label='Rectangle 2')
plt.plot(rect_1_19_time,rect_1_19_nsi,'x',linestyle='None',label='Rectangle 3')
plt.legend(prop={'size': 16},frameon=False,borderpad=0, handletextpad=0, loc='lower right')
plt.xlabel('Time (s)', size=16)
plt.ylabel('Nucleus Shape Index', size=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.yticks(np.arange(0.8, 1.1, 0.1))
plt.xticks(np.arange(0, 110, 100))
plt.ylim(0.8,1)
plt.savefig('nsi_time.pdf',format='pdf', bbox_inches='tight')
plt.show()
print(final_data)
df = pd.DataFrame(final_data)
df.to_csv('csi_nsi_1_55.csv', index = False)
plt.figure(2)
plt.plot(final_data[:,0],final_data[:,1],'-ks', label='Simulation')
plt.plot(literature_data['CSI.1'].values,literature_data['NSI.1'].values,':o', label='Exp:U2OS')
plt.plot(literature_data['CSI.2'].values,literature_data['NSI.2'].values,':x', label='Exp:hMSC')
plt.plot(literature_data['CSI.3'].values,literature_data['NSI.3'].values,':*', label='Exp:EC')
plt.legend(prop={'size': 16})
plt.xlabel('CSI', size=16)
plt.ylabel('NSI', size=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.yticks(np.arange(0.5, 1.1, 0.5))
plt.xticks(np.arange(0.2, 1.1, 0.4))
plt.savefig('csi_nsi.pdf',format='pdf', bbox_inches='tight')
plt.show()
