import  pdb
import numpy as np
import math
import matplotlib.pyplot as plt
import csv
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

earth_rad = 63741 #km
degree_rad = 180.0/3.14159
onedeg_latt_dist = earth_rad * 3.14158/180.0

class cloud():
  reflect = 0.25
  sea = 0.67
  land = 0.5

  
class latluts:
    lattitude = [-90.0,-80.0,-70.0,-60.0,-50.0,-40.0,-30.0,-20.0,-10.0, 0.0,
                 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]
    albedo = [0.73, 0.73, 0.4, 0.18, 0.15, 0.12, 0.12, 0.12, 0.11, 0.11,
              0.12, 0.15, 0.17, 0.16, 0.2, 0.30, 0.42, 0.52, 0.58]
    power = [131.6666667,167.1875,197.7083333,233.8541667,280.9375,326.1458333,
             362.3958333,391.7708333,409.375,414.5833333,411.0416667,395,
             366.9791667,331.9791667,287.9166667,241.6666667,206.25,176.1458333,
              140.7291667]

def albbylat(lattitude):
    return np.interp(lattitude, latluts.lattitude, latluts.albedo)

def area_by_latt_band(latt, width):
  rad_at_top = math.cos(latt/degree_rad) * earth_rad
  rad_at_bottom =  math.cos((latt+width)/degree_rad) * earth_rad
  area = 3.14159 * (rad_at_top + rad_at_bottom) * width * onedeg_latt_dist
  return area

def global_power_check():
  areas = [];VIS_power = 0.0; IR_power = 0.0; netup = 0.0;
  angles = [0.0, 5.0, 15.0, 25.0, 35.0, 45.0, 55.0, 65.0, 75.0, 85.0]
  widths = [5.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 5.0]
  temps = [25.0, 21.0, 16.0, 12.0, 8.0, 5.0,  3.0,  -4.0, -10.0, -20.0]
  for ix in range(len(angles)):
     latchk = angles[ix] + (widths[ix]/2.0)
     tot, vis, ir, ab  = rawPower(latchk)
     areas.append(area_by_latt_band(angles[ix], widths[ix]))
     VIS_power += areas[ix] * vis
     IR_power +=  areas[ix] * ir
     tot, vis, ir, ab = rawPower(-latchk)
     VIS_power += areas[ix] * vis
     IR_power +=  areas[ix] * ir
     netup += areas[ix] * netIRup(temps[ix])
     netup += areas[ix] * netIRup(temps[ix])    
  areas = np.array(areas)
  print('global average VIS w/m2:', (VIS_power / (2 * areas.sum())))
  print('global average IR w/m2:', (IR_power / (2 * areas.sum())))
  print('global average net IR up w/m2:', (netup / (2 * areas.sum())))
  print('total area: ', areas.sum())
  print('check quotient:',(2.0 *3.14159 * earth_rad * earth_rad) / areas.sum())
  print areas
  
#  https://scienceofdoom.com/2010/07/17/the-amazing-case-of-back-radiation/
def IR_down(lat):
  _powers = [120.0, 320.0, 400, 320,120.0]
  _latts = [-90.0,-60, 0, 60.0, 90.0 ]
  P = 0.955 *  np.interp(lat, _latts, list(_powers))
  return P

def IR_abs(lat):
  _apowers = [30.0, 78.0, 100, 78.0, 30.0]
  _alatts = [ -90.0,-60, 0, 60.0, 90.0 ]
  P =   np.interp(lat, _alatts, list(_apowers))
  return P

#https://www.giss.nasa.gov/research/briefs/rossow_01/distrib.html  
def rawPower(lat, land= 0.5, sea=0.5):
  P = 0.955 *  np.interp(lat, latluts.lattitude, list(reversed(latluts.power)))
  refloss = cloud.reflect *((land*cloud.land)+(sea*cloud.sea))
  abloss = IR_abs(lat)
  VIS = ((P*(1-refloss))- abloss)  * (1-albbylat(lat))
  IR = IR_down(lat)
  return VIS + IR, VIS, IR, abloss

def netIRup(tem):  #approximate for sealevel
  sb = 5.67 * ((tem + 273.15)**4)/ 100000000.0
  #print(0.16*sb)
  if tem > -1:
    return 0.155 * sb
  elif tem > -3:  #dry sky blow torch
    return 0.22  * sb
  else:
    return 0.3 * sb

  
class climSensDataset():
  def __init__(self, fname):
    df = pd.read_csv(fname)
    self.Names = df.Name
    self.Longitude = df.Longitude
    self.Lattitude = df.Latitude
    self.Elevations = df.Elevation
#    self.Power = df.PowerA
    self.GISStemp = df.GISStemp
    self.gt = np.array(self.GISStemp)
    self.Power0 = []; self.Power =[]; self.IRPwr = [];
    for ix in range(len(self.Lattitude)):
      tot, vis, ir, ab = rawPower(self.Lattitude[ix])
      netup = netIRup(self.GISStemp[ix])
      self.Power.append(vis-netup)
      self.IRPwr.append(ir)
      self.Power0.append(vis + ab)
      #self.truePower.append(self.Power[ix] * (1-albbylat(self.Lattitude[ix])))

      #remove Amundsen Scott,8,-89,3000,141,-32.5,39.48,0.72,141,6.770142817

nh = climSensDataset('NH_dataset.csv')
sh = climSensDataset('SH_dataset.csv')
ha = climSensDataset('HA_dataset.csv')
#print nh.Names
#print nh.truePower
#print nh.GISStemp
ipccT = []; ipccP = [];
for ix in range(50):
  ipccT.append( -10.0 + (ix*0.8))
  ipccP.append(0 + ix)

plt.title('Temperature vs Power[VIS+IR] at surface stations')
plt.xlabel('Power (watts/meter^2)')
plt.ylabel('Station temperature (C)')
plt.scatter(nh.Power,nh.gt, s=40, c='b', marker= 'o', label='N Hemi')
plt.scatter(sh.Power, sh.gt,s=40,  c='r', marker= 's', label = 'S Hemi')
plt.scatter(ha.Power, ha.gt,s=40,  c='g', marker= 's', label = 'Hi Alt')
plt.scatter(ipccP, ipccT, s = 20, c='g', marker = 'x', label= 'IPCC best')

CO2doubPwr = [40.0, 41.5, 43.7]
CO2DoubTemp  = [20.0,20.0,20.0]

plt.scatter(CO2doubPwr, CO2DoubTemp, s = 20, c='k', marker = '_', label= 'CO2 double')

for ix in range(100):
  ipccT.append( -10.0 + (ix*0.4))
  ipccP.append(0 + ix)

#automated QC check  
global_power_check()
                 
plt.scatter(ipccP, ipccT, s = 20, c='g', marker = 'x', label= 'IPCC Low')                 
plt.legend(loc='lower right')

#pdb.set_trace()
print('sensitivites to VIS + IR  power')
fit = np.polyfit(nh.Power, nh.GISStemp, 1)
print('NH sens:' + str(fit))

fit = np.polyfit(sh.Power, sh.GISStemp, 1)
print('SH sens:' + str(fit))

print('sensitivites to VIS + AB  power')
fit = np.polyfit(nh.Power0, nh.GISStemp, 1)
print('NH sens:' + str(fit))

fit = np.polyfit(sh.Power0, sh.GISStemp, 1)
print('SH sens:' + str(fit))

print('sensitivites to IR only power')
fit = np.polyfit(nh.IRPwr, nh.GISStemp, 1)
print('NH sens:' + str(fit))

fit = np.polyfit(sh.IRPwr, sh.GISStemp, 1)
print('SH sens:' + str(fit))

plt.show()
