import  pdb
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


class albedo:
    lattitude = [-90.0,-80.0,-70.0,-60.0,-50.0,-40.0,-30.0,-20.0,-10.0, 0.0,
                 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]
    albedo = [0.73, 0.73, 0.4, 0.18, 0.15, 0.12, 0.12, 0.12, 0.11, 0.11,
              0.12, 0.15, 0.17, 0.16, 0.2, 0.30, 0.42, 0.52, 0.58]

def albbylat(lattitude):
    return np.interp(lattitude, albedo.lattitude, albedo.albedo)

class climSensDataset():
  def __init__(self, fname):
    df = pd.read_csv(fname)
    self.Names = df.Name
    self.Longitude = df.Longitude
    self.Lattitude = df.Latitude
    self.Elevations = df.Elevation
    self.Power = df.Power
    self.GISStemp = df.GISStemp
    self.gt = np.array(self.GISStemp)
    self.truePower = []
    for ix in range(len(self.Lattitude)):
      self.truePower.append(self.Power[ix] * (1-albbylat(self.Lattitude[ix])))
    self.truePower = np.array(self.truePower)

nh = climSensDataset('NH_dataset.csv')
sh = climSensDataset('SH_dataset.csv')
#print nh.Names
#print nh.truePower
#print nh.GISStemp
ipccT = []; ipccP = [];
for ix in range(50):
  ipccT.append( -10.0 + (ix*0.8))
  ipccP.append(180 + ix)

plt.title('Temperature vs Power at surface stations')
plt.xlabel('Power (watts/meter^2)')
plt.ylabel('Station temperature (C)')
plt.scatter(nh.Power,nh.gt, s=40, c='b', marker= 'o', label='NH')
plt.scatter(sh.Power, sh.gt,s=40,  c='r', marker= 's', label = 'SH')
plt.scatter(ipccP, ipccT, s = 20, c='g', marker = 'x', label= 'IPCC')

for ix in range(100):
  ipccT.append( -10.0 + (ix*0.4))
  ipccP.append(180 + ix)

plt.scatter(ipccP, ipccT, s = 20, c='g', marker = 'x', label= 'IPCC')

plt.legend(loc='lower right')
print('Albedo cotrrected sensitivities')
fit = np.polyfit(nh.truePower, nh.GISStemp, 1)
print('NH sens:' + str(fit))

fit = np.polyfit(sh.truePower, sh.GISStemp, 1)
print('SH sens:' + str(fit))

#pdb.set_trace()
print('sensitivites on raw input solar power')
fit = np.polyfit(nh.Power, nh.GISStemp, 1)
print('NH sens:' + str(fit))

fit = np.polyfit(sh.Power, sh.GISStemp, 1)
print('SH sens:' + str(fit))


plt.show()
