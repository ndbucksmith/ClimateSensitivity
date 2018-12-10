import  pdb
import numpy as np
import matplotlib.pyplot as plt

#pdb.set_trace()

class nhDS():  #north hemi climate sens data set
  names = ['Dudinka', 'Ft_Yukon', 'Moskva', 'Eddinugh', 'Dublin', 'Cambridge', 'Norfolk',
           'Ponca_City', 'Tokyo', 'Madison', 'Kuwait', 'Agra', 'Key_West', 'Goa',
           'Bangalore', 'Maturin', 'Tamale_W_Africa', 'Dahomey','Sao_Gabriel',]
  GISStemps = [-10.0, -6.0, 5.0, 8.5, 9.0, 9.5, 16, 15.0, 15.0, 20.0, 28.0,
	        26.0,  25.0, 27.5, 24.0, 27.5, 28.0, 26.0, 26.0]
  TOApower = [200, 210.0, 256.0, 257.0,	268.0, 272.0, 333.0, 333.0, 330.0,
              360.0, 364.0, 370.0, 377.0,400, 405.0, 409.0, 410.0, 412.0, 414.0]
  latt = [69.4, 66, 55, 55.5, 53.4, 52.2, 37, 36.7,
          35.7,30.4, 29.5, 27.7, 24.6, 15.5, 13, 9.8, 9.4, 8.4, 0]

print  len(nhDS.names)
print len(nhDS.GISStemps)
print len(nhDS.TOApower)
print len(nhDS.latt)

class albedo:
    lattitude = [-90.0,-80.0,-70.0,-60.0,-50.0,-40.0,-30.0,-20.0,-10.0, 0.0,
                 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]
    albedo = [0.73, 0.73, 0.4, 0.18, 0.15, 0.12, 0.12, 0.12, 0.11, 0.11,
              0.12, 0.15, 0.17, 0.16, 0.2, 0.30, 0.42, 0.52, 0.58]

print  len(albedo.lattitude)
print len(albedo.albedo)

def albbylat(lattitude):
    return np.interp(lattitude, albedo.lattitude, albedo.albedo)

print albbylat(10)
print albbylat(69)
print albbylat(-40)


    
