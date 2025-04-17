import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data_1_5 = pd.read_csv("csi_nsi_1_5.csv")
csi_1_5=data_1_5['0'].values
nsi_1_5=data_1_5['1'].values

data_1_55 = pd.read_csv("csi_nsi_1_55.csv")
csi_1_55=data_1_55['0'].values
nsi_1_55=data_1_55['1'].values

data_1_6 = pd.read_csv("csi_nsi_1_6.csv")
csi_1_6=data_1_6['0'].values
nsi_1_6=data_1_6['1'].values

data_1_65 = pd.read_csv("csi_nsi_1_65.csv")
csi_1_65=data_1_65['0'].values
nsi_1_65=data_1_65['1'].values

csi_data = [csi_1_5,csi_1_55,csi_1_6,csi_1_65]
print(csi_data)
csi_mean=np.mean(csi_data,axis=0)
csi_std=np.std(csi_data,axis=0)
#print(csi_mean)
#print(csi_std)
nsi_data= [nsi_1_5,nsi_1_55,nsi_1_6,nsi_1_65,nsi_1_65]
nsi_mean=np.mean(nsi_data,axis=0)
nsi_std=np.std(nsi_data,axis=0)
print(nsi_data)
#print(nsi_mean)
#print(nsi_std)

literature_data = pd.read_excel('nsi_csi_data.xlsx')
print(literature_data)
plt.plot(csi_mean,nsi_mean,'-ks', label='Simulation')
plt.fill_between(csi_mean, (nsi_mean-nsi_std), (nsi_mean+nsi_std), color='black', alpha=0.1)
plt.plot(literature_data['CSI.1'].values,literature_data['NSI.1'].values,':o', label='Exp:U2OS')
plt.plot(literature_data['CSI.2'].values,literature_data['NSI.2'].values,':x', label='Exp:hMSC')
plt.plot(literature_data['CSI.3'].values,literature_data['NSI.3'].values,'--*', label='Exp:EC')
plt.legend(prop={'size': 16})
plt.xlabel('CSI', size=16)
plt.ylabel('NSI', size=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.savefig('csi_nsi_u2os.pdf',format='pdf', bbox_inches='tight')
plt.show()

