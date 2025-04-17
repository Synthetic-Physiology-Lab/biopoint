import numpy as np
import matplotlib.pyplot as plt
import math


xx=[0.5, 0.75]
yy=[82, 9] 
plt.bar(xx, yy, width=0.2, color='black')
plt.tick_params(axis='x', labelsize=16)
plt.tick_params(axis='y', labelsize=16)
plt.xlabel('')
plt.ylabel('% Particles', size=16)
plt.ylim(0,100)
#plt.legend(prop={'size': 16})
#plt.title('Cytoplasmic particles inside nuclear surface')
plt.savefig('nuc_part_phase_sep.pdf',bbox_inches='tight')
plt.show()    
